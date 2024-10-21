from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from etl import create_update_dm_crypto_table  # Importamos la función

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

# Definimos el DAG
dag = DAG(
    'create_update_dm_crypto_table',
    default_args=default_args,
    description='DAG para crear/actualizar la tabla data mart de criptos',
    schedule_interval='@daily',
    catchup=False,
)

# Sensor para esperar la finalización del DAG `transform_load_crypto_data`
wait_for_transform_load = ExternalTaskSensor(
    task_id='wait_for_transform_load',
    external_dag_id='transform_load_crypto_data',
    external_task_id='transform_load_crypto_data',
    timeout=1200,  # Tiempo de espera máximo
    poke_interval=30,  # Verificar cada 30 segundos
    mode='poke',  # Espera activa
    execution_date_fn=lambda dt: dt,  # Asegura que la fecha de ejecución coincida
    dag=dag,
)

# Definimos la tarea de creación/actualización de la tabla data mart
create_update_task = PythonOperator(
    task_id='create_update_dm_crypto_table',
    python_callable=create_update_dm_crypto_table,
    dag=dag,
)

# Definimos la dependencia: el sensor debe completarse antes de crear la tabla
wait_for_transform_load >> create_update_task