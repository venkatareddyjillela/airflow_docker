from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retries_delay': timedelta(minutes=5)
}


@dag(dag_id='our_first_dag_api_v1',
     default_args=default_args,
     description="Our first DAG",
     start_date=datetime(2022, 10, 3, 20),
     schedule_interval='@daily')
def our_first_dag_v2():

    @task(multiple_outputs=True)
    def get_name():
        return {
            'firstname': 'venkata reddy',
            'lastname': "jillela"
        }

    @task
    def get_age():
        return 22

    @task()
    def greet(firstname, lastname, age):
        print(f'Hello {firstname} {lastname} you are {age} years old !!!!')

    name_dict = get_name()
    age = get_age()
    greet(firstname=name_dict['firstname'],
          lastname=name_dict['lastname'], age=age)


greet_dag = our_first_dag_v2()
