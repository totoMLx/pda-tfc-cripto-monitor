from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from etl import transform_load_crypto_data 

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

# Definimos el DAG de transformación y carga
dag = DAG(
    'transform_load_crypto_data',
    default_args=default_args,
    description='DAG para transformar y cargar los datos de criptoactivos en Redshift',
    schedule_interval='@daily',
    catchup=False
)

wait_for_extract = ExternalTaskSensor(
    task_id='wait_for_extract',
    external_dag_id='extract_crypto_data',
    external_task_id='extract_crypto_data',  # Asegúrate de que el nombre coincida
    timeout=600,  # Tiempo de espera en segundos
    poke_interval=30,  # Intervalo de verificación en segundos
    mode='poke',  # 'poke' o 'reschedule' según tu caso de uso
    execution_date_fn=lambda dt: dt,  # Usa la misma fecha de ejecución
    dag=dag,
)

# Definimos la tarea de transformación y carga
transform_load_task = PythonOperator(
    task_id='transform_load_crypto_data',
    python_callable=transform_load_crypto_data,
    dag=dag,
)

# Definimos las dependencias entre tareas
wait_for_extract >> transform_load_task