from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sys
sys.path.append("/criminal_minds/Dags/dags")
from Extract import Extract
from Dimentionalmodel import load_to_postgres
from Kafka_tasks import start_produce
from Api import(
    Extract as api_Extract,
    Transform as api_Transform,
    Load as api_load
)


default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2024, 10, 2),
    'email_on_failure': False,
    'email_on_rety':False,
    'retries':1,
    'retry_delay': timedelta(seconds=10)
}

dag = DAG(
    'Proyect_ETL_Criminal_Minds',
    default_args=default_args,
    description='Etl process Dimentional Model',
    schedule_interval=timedelta(days=1),
)

def log_task_execution(task_name, **kwargs):
    print(f"Executing task:{task_name}")


with dag:
    extract_data = PythonOperator(
        task_id='Extract_data',
        python_callable=Extract,
    )
    charge_dimentional_model= PythonOperator(
        task_id = 'Dimentional_model',
        python_callable=load_to_postgres,
        #provide_context=True
    )
    extract_api_data = PythonOperator(
        task_id='Extract_api_data',
        python_callable=api_Extract
    )
    transform_api_data = PythonOperator(
        task_id='Transform_api_data',
        python_callable=api_Transform,
        #provide_context=True
    )
    load_api_data=PythonOperator(
        task_id='Load_api_data',
        python_callable=api_load,
        #provide_context=True
    )
    producer_kafka=PythonOperator(
        task_id='Producer_kafka',
        python_callable=start_produce,
        #provide_context=True
    )

    extract_data >> charge_dimentional_model >> producer_kafka
    extract_api_data >> transform_api_data >> load_api_data #>> producer_kafka