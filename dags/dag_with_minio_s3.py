from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='dag_with_minio_s3_v2',
    default_args=default_args,
    description="Our first DAG",
    start_date=datetime(2022, 10, 1, 20),
    schedule_interval='@daily'
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn',
        mode='poke',
        poke_interval=5,
        timeout=60
    )

