from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}


def get_sklearn():
    import sklearn
    print("sklearn version: {}".format(sklearn.__version__))


with DAG(
    dag_id='dag_with_python_dependencies',
    default_args=default_args,
    description="dag_with_python_dependencies",
    start_date=datetime(2022, 10, 1, 20),
    schedule_interval='@daily'
) as dag:
    get_sklearn_task = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn

    )
get_sklearn_task
