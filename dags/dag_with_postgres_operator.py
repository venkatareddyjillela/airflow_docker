from asyncio import tasks
from datetime import datetime, timedelta
# from airflow.decorators import dag, task

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_postgres_v3',
    default_args=default_args,
    description="Our first DAG",
    start_date=datetime(2022, 10, 1, 20),
    schedule_interval='0 0 * * *'

) as dag:
    task1 = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists dag_runs(
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )

    task2 = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='postgres_localhost',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ds}}', '{{dag.dag_id}}')
        """
    )

    task3 = PostgresOperator(
        task_id='delete_data_from_table_dag_runs',
        postgres_conn_id='postgres_localhost',
        sql="""
            delete from dag_runs where dt = '{{ds}}' and dag_id = '{{dag.dag_id}}'
        """
    )

    task1 >> task3 >> task2
