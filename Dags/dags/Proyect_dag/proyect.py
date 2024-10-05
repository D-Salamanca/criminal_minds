from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
import sys
sys.path.append("/home/joan/Desktop/Proyect-ETL/criminal_minds/Dags/dags")
from Extract import Extract
from Dimentionalmodel import load_to_postgres

default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2024, 10, 2),
    'email_on_failure': False,
    'email_on_rety':False,
    'retries':3,
    'retry_delay': timedelta(minutes=5)
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
        provide_context=True
    )
    extract_data >> charge_dimentional_model