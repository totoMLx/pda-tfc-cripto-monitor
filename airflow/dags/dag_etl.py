from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from etl import extract_crypto_data, transform_load_crypto_data, create_update_dm_crypto_table

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

# Definimos el DAG unificado
dag = DAG(
    'etl_crypto_pipeline',
    default_args=default_args,
    description='Pipeline completo para extraer, transformar y cargar datos de criptoactivos',
    schedule_interval='@daily',
    catchup=False,
)

# Tarea 1: Extracción de datos
extract_task = PythonOperator(
    task_id='extract_crypto_data',
    python_callable=extract_crypto_data,
    dag=dag,
)

# Tarea 2: Transformación y carga de datos
transform_load_task = PythonOperator(
    task_id='transform_load_crypto_data',
    python_callable=transform_load_crypto_data,
    dag=dag,
)

# Tarea 3: Crear/Actualizar la tabla data mart
create_update_task = PythonOperator(
    task_id='create_update_dm_crypto_table',
    python_callable=create_update_dm_crypto_table,
    dag=dag,
)

# Definimos las dependencias para ejecutar las tareas en secuencia
extract_task >> transform_load_task >> create_update_task