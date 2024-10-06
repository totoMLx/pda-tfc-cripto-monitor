import pandas as pd
import requests
import os
from datetime import datetime
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

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

def get_crypto_symbols(ninja_key):
    """Usamos la API de ninja para ir a buscar todos los simbolos de los cripto activos que queremos consultar"""
    symbols_url = 'https://api.api-ninjas.com/v1/cryptosymbols'
    response = requests.get(symbols_url, headers={'X-Api-Key': ninja_key})
    if response.status_code == 200:
        return response.json()['symbols']
    else:
        print("Error:", response.status_code, response.text)
        return []

def get_crypto_price(ninja_key, symbol):
    """Con los simbolos de los cripto activos, vamos a buscar el precio actual de cada uno"""
    price_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
    response = requests.get(price_url, headers={'X-Api-Key': ninja_key})
    if response.status_code == 200:
        data = response.json()
        return data['symbol'], data['price']
    else:
        print("Error:", response.status_code, response.text)
        return symbol, None
    
def create_append_to_table(df, name, engine, schema):
    df.to_sql(name=name, con=engine, schema=schema, if_exists='append', index=False)


def insert_crypto_data(engine):
    """Insertar el precio de cada cripto activo dentro de la tabla que contiene el precio historico de cada uno"""
    ninja_key = get_env_variable('NINJA_API_KEY')
    symbols = get_crypto_symbols(ninja_key)
    
    crypto_prices = pd.DataFrame(columns=['symbol', 'price_USD', 'date'])
    crypto_prices['symbol'] = symbols

    for row in range(len(crypto_prices)):
        symbol = crypto_prices['symbol'][row]
        symbol_check,price = get_crypto_price(ninja_key, symbol)
        today_date = datetime.now()
        date_str = today_date.strftime('%Y-%m-%d %H:%M:%S')
        if symbol_check == symbol:
                crypto_prices.at[row,'price_USD'] = round(float(price),3)
                crypto_prices.at[row, 'date'] = date_str
        else:
            crypto_prices.at[row,'price'] = -1
            crypto_prices.at[row, 'date'] = date_str
            
    create_append_to_table(crypto_prices, 'crypto_prices', engine, '2024_tomas_fernando_campi_schema')


if __name__ == '__main__':
    engine = create_db_engine()
    insert_crypto_data(engine)