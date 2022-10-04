from datetime import datetime,timedelta


from airflow import DAG

#  import bash operator from airflow
# from airflow.operators.bash import BashOperator

# import python operator from airflow
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}

def greet(ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'Hello {first_name} {last_name} you are {age} years old')

def get_name(ti):
    ti.xcom_push(key='first_name', value='Venkata Reddy')
    ti.xcom_push(key='last_name', value='Jillela')
    
def get_age(ti):
    ti.xcom_push(key='age', value=25)

with DAG(
    dag_id = 'our_first_dag_v1',
    default_args = default_args,
    description= "Our first DAG",
    start_date = datetime(2022, 10, 3,20),
    schedule_interval = '@daily'
) as dag:
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable = greet
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age
    )


    [task2, task3] >> task1
