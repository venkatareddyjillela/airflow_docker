from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='our_first_dag__catchup_v2',
    default_args=default_args,
    description="Our first DAG",
    start_date=datetime(2022, 10, 3, 20),
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='greet',
        bash_command='echo "Hello World"'
    )
