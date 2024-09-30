from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ensuring the scripts directory is in the path so that our module can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from crypto_app import insert_crypto_data  # Import the function

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'insert_crypto_data_redshift',
    default_args=default_args,
    description='DAG que envia la informacion sobre los distintos cripto activos del dia a redshift',
    schedule_interval='@daily',
    catchup=False
)

send_data = PythonOperator(
    task_id='insert_crypto_data_redshift',
    python_callable=insert_crypto_data,
    dag=dag,
)

send_data