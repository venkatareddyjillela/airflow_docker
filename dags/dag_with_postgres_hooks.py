
from datetime import datetime, timedelta

from airflow import DAG
import csv
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from tempfile import NamedTemporaryFile

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}


def postgres_to_s3(ds_nodash, next_ds_nodash):
    # step 1: get data from postgres and save it to a txt file
    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("select * from orders where date >= %s and date < %s",
                   (ds_nodash, next_ds_nodash))
    with NamedTemporaryFile(mode='w', suffix=f"{ds_nodash}") as f:
        # with open(f'dags/get_orders_{ds_nodash}.txt', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("saved orders data to file : %s",
                     f"dags/get_orders_{ds_nodash}.txt")

        # step 2: upload the file to s3
        s3_hook = S3Hook(aws_conn_id='minio_conn')
        s3_hook.load_file(
            filename=f.name,
            key=f"orders_{ds_nodash}.txt",
            bucket_name='airflow',
            replace=True
        )
        logging.info("Orders file %s has been uploaded to s3", f.name)


with DAG(
    dag_id='dag_with_postgres_hooks_v3',
    default_args=default_args,
    description="Our first DAG",
    start_date=datetime(2022, 10, 1, 20),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )

    task1
