from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_with_cron_expression_v1',
    default_args=default_args,
    description="Our first DAG",
    start_date=datetime(2022, 9, 3, 20),
    schedule_interval='0 0 * * *'
) as dag:
    task1 = BashOperator(
        task_id='greet',
        bash_command='echo "Hello World"'
    )

    task1
