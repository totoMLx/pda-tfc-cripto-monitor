# README - ETL Crypto Prices


## Descripción

El objetivo principal del proyecto es crear un ETL a partir de APIs OpenSource (api-ninjas, dolarapiy coinmarketcap api). El mismo consume data tanto de los precios de cripto activos, informacion de los activos y el valor del dolar blue. El resultado del proyecto son cuatro tablas que se actualizan diariamente (cuando el proceso se encuentra encendido):

    1. bt_crypto_prices: la misma tiene los valores de varios cripto activos en USD y en pesos argentinos. El proceso esta hecho para obtener los precios de una gran variedad de cripto activos pero por cuestiones de quota de la API, esta limitado unicamente a traer los de BTC, ETH y DOGE.
    2. bt_dolar_prices: tabla que contiene los valores historicos del dolar (tipo de cambio blue). Cada vez que se realiza una consulta para el precio de algun cripto activo, se actualiza el valor del dolar en esta tabla. La misma permite tener un registro de la variacion del precio a lo largo del tiempo para, en caso de ser deseado, consultar el valor en pesos de cada cripto activo en x momento en el tiempo.
    3. lk_crypto_data: la misma contiene informacion de cada una de las criptos al dia de la fecha. En la tabla se encuentran los siguientes campos: 
        - price_usd: indica el precio del activo en dolares [USD]
        - price_pesos: indica el precio del activo en pesos (conversion con dolar blue al dia del registro) [pesos]
        - market_cap; capitalizacion del mercado para el cripto activo [USD]
        - cmc_dominance: porcentaje que representa el market_cap del activo por sobre el market_cap de todo el ecosistema critpto [%]
        - cmc_rank: ranking del market_cap del activo en el top de criptos [rank]
        - fiat_flag: flag que declara si es una moneda fiat [bool]
    4. dm_crypto_daily_information: tabla que agrupa para el dia corriente toda la informacion para las 3 criptos disponibles (BTC, ETH, DOGE)

Todo el codigo para el funcionamiento del proyecto se encuentra en la carpeta 'airflow'.
A continuación se adjunta diagrama de funcionamiento:

![etl](https://github.com/user-attachments/assets/4e154c63-bbca-4cca-a028-dcdbadb94101)

El script `dag_etl.py` ejectura las 3 tareas para la extraccion, transformacion y carga de datos. Las tareas extract_crypto_data, transform_load_crypto_data y create_update_dm_crypto_table que crea la tabla data mart. Las funciones que ejecutan las tareas se encuentran dentro de `etl.py` Las funciones complementarias para que el proceso sea posible, se encuentran en `utils.py`.


---

## Estructura del repositorio

En el proyecto hay 2 carpetas principales:
- `airflow` la cual contiene todo el codigo para ejecutar el pipeline
- `tests` la cual contiene los test unitarios para asegurarse que todo funcione correctamente

Dentro de `airlow` la estructura es la siguiente:

- **dags/**: Tiene la DAG para orquestar las tareas en Airflow.
- **scripts/**:
  - **etl.py**: El archivo principal del proceso ETL. En el mismo se extrae la informacion de las apis, se transforman los numeros en formato mas legible, se utiliza la api de dolar-api para obtener el valor en pesos del cripto activo. Finalmente se suben los datos a las tres tablas que se encuentran en Redshift y se crea la tabla de data mart
  - **utils.py**: Este archivo tiene todas las funciones auxiliares, las cuales son importadas y ejecutadas por etl.py
  - **config.py**: Este archivo contiene info de configuracion de los simbolos de las criptos que se va a consultar la informacion
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
export CMC_API_KEY=cmc-api-key-compartida
```

### 4. Ejecutar el ETL

Ejecutar desde **Airflow** con **Docker** levantando el contenedor:

```bash
docker-compose up --build
```
