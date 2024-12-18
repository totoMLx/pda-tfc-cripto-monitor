import os
import requests
import json
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def get_env_variable(var_name):
    """Devolver las variables de entorno"""
    try:
        return os.environ[var_name]
    except KeyError:
        raise EnvironmentError(f"Error seteando la variable de entorno {var_name}.")
    
    
def create_db_engine():
    """Conexion con redshift y creacion del engine con sqlalchemy"""
    user = quote_plus(get_env_variable('REDSHIFT_USER'))
    password = quote_plus(get_env_variable('REDSHIFT_PASSWORD'))
    host = get_env_variable('REDSHIFT_HOST')
    port = get_env_variable('REDSHIFT_PORT')
    database = get_env_variable('REDSHIFT_DB')
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)

    
    
def create_append_to_table(df, name, engine, schema):
    """Insertar o añadir datos a la tabla SQL"""
    df.to_sql(name=name, con=engine, schema=schema, if_exists='append', index=False)

        

def get_crypto_price(ninja_key, symbol):
    """Obtener el precio actual de cada criptoactivo por símbolo"""
    price_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
    response = requests.get(price_url, headers={'X-Api-Key': ninja_key})
    response.raise_for_status()
    data = response.json()
    return data.get('symbol'), data.get('price')

def get_dolar_price():
    """API para obtener el precio del dolar blue al momento de la consulta"""
    response = requests.get("https://dolarapi.com/v1/dolares/blue")
    return response.json()
    
def get_crypto_data(cmc_key, id):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
    'id':f'{id}'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': f'{cmc_key}',
    }

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return data
    
    