# README - ETL Crypto Prices


## Descripción

El objetivo principal del proyecto es crear un ETL a partir de APIs OpenSource (api-ninjas y dolarapi). El mismo consume data tanto de los precios de cripto activos como el valor del dolar blue. El resultado del proyecto son dos tablas que se actualizan diariamente (cuando el proceso se encuentra encendido):

    1. crypto_prices: la misma tiene los valores de varios cripto activos en USD y en pesos argentinos. El proceso esta hecho para obtener los precios de una gran variedad de cripto activos pero por cuestiones de quota de la API, esta limitado unicamente a traer los de BTC, ETH y DOGE.
    2. dolar_prices: tabla que contiene los valores historicos del dolar (tipo de cambio blue). Cada vez que se realiza una consulta para el precio de algun cripto activo, se actualiza el valor del dolar en esta tabla. La misma permite tener un registro de la variacion del precio a lo largo del tiempo para, en caso de ser deseado, consultar el valor en pesos de cada cripto activo en x momento en el tiempo.

Todo el codigo para el funcionamiento del proyecto se encuentra en la carpeta 'airflow'.
A continuación se adjunta diagrama de funcionamiento:

[imagen]


El script `dag_etl.py` ejectura la funcion insert_crypto_data de `etl.py` la cual se encarga de buscar la data en las APIs correspondientes, transformar la data y enviarla a la base de datos de Redshift. Las funciones complementarias para que el proceso sea posible, se encuentran en `utils.py`.


---

## Estructura del repositorio

En el proyecto hay 2 carpetas principales:
- `airflow` la cual contiene todo el codigo para ejecutar el pipeline
- `tests` la cual contiene los test unitarios para asegurarse que todo funcione correctamente

Dentro de `airlow` la estructura es la siguiente:

- **dags/**: Tiene la DAG para orquestar las tareas en Airflow.
- **scripts/**:
  - **etl.py**: El archivo principal del proceso ETL. En el mismo se extrae la informacion de las apis, se transforman los numeros en formato mas legible, se utiliza la api de dolar-api para obtener el valor en pesos del cripto activo. Finalmente se suben los datos a las dos tablas que se encuentran en Redshift.
  - **utils.py**: Este archivo tiene todas las funciones auxiliares, las cuales son importadas y ejecutadas por etl.py
- **logs**: contiene los logs de los dags ejectuados en RedShift
---


## Instrucciones para reproducir el proceso

### 1. Clonar el repo

```bash
git clone https://github.com/totoMLx/pda-tfc-cripto-monitor.git
```

### 2. Instalar las dependencias con pip

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales

- Las credenciales son compartidas por medio externo (slack) con el fin de preservar la seguridad del proyecto
- Configurar las variables de entorno para poder acceder a las APIs utilizadas en el proyecto:

```bash
export NINJA_API_KEY=api-compartida
export REDSHIFT_HOST=host-compartido
export REDSHIFT_USER=usuario-compartido
export REDSHIFT_PASSWORD=password-compartido
export REDSHIFT_DB=database-compartida
export REDSHIFT_PORT= port-compartido
```

### 4. Ejecutar el ETL

Ejecutar desde **Airflow** con **Docker** levantando el contenedor:

```bash
docker-compose up --build
```