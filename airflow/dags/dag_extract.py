from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Aseguramos que la carpeta 'scripts' esté en el path para poder importar nuestros módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from etl import extract_crypto_data  # Importamos la función de extracción

# Argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definimos el DAG de extracción
dag = DAG(
    'extract_crypto_data',
    default_args=default_args,
    description='DAG para extraer los datos de criptoactivos y guardarlos en parquet',
    schedule_interval='@daily',
    catchup=False
)

# Definimos la tarea de extracción
extract_task = PythonOperator(
    task_id='extract_crypto_data',
    python_callable=extract_crypto_data,
    dag=dag,
)

extract_task 