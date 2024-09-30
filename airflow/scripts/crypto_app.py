import pandas as pd
import requests
import os
import json
from datetime import datetime
from urllib.parse import quote_plus
from sqlalchemy import create_engine

ninja_key = os.getenv('NINJA_API_KEY')
user = quote_plus(os.getenv('REDSHIFT_USER'))
password = quote_plus(os.getenv('REDSHIFT_PASSWORD'))
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT')
database = os.getenv('REDSHIFT_DB')

# Ensure you have all necessary variables defined: user, password, host, port, database, and schema.
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
# Create the engine using SQLAlchemy
engine = create_engine(connection_string)

def get_crypto_symbols():
    symbols = 'https://api.api-ninjas.com/v1/cryptosymbols'
    response = requests.get(symbols, headers={'X-Api-Key': ninja_key})
    if response.status_code == requests.codes.ok:
        return json.loads(response.text)['symbols']
    else:
        print("Error:", response.status_code, response.text)
        return None


def get_crypto_price(symbol):
    price_url = 'https://api.api-ninjas.com/v1/cryptoprice?symbol={}'.format(symbol)
    response = requests.get(price_url, headers={'X-Api-Key': ninja_key})
    if response.status_code == requests.codes.ok:
        symbol_ret =json.loads(response.text)['symbol']
        price_ret =json.loads(response.text)['price']
        return symbol_ret, price_ret
    else:
        print("Error:", response.status_code, response.text)
        return None
    
def create_append_to_table(df, name, engine, schema):
    df.to_sql(name=name, con=engine, schema=schema, if_exists='append', index=False)

def insert_crypto_data():
    symbols = get_crypto_symbols()

    crypto_prices = pd.DataFrame(columns=['symbol', 'price_USD', 'date'])
    crypto_prices['symbol'] = symbols

    for row in range(len(crypto_prices)):
        symbol = crypto_prices['symbol'][row]
        symbol_check,price = get_crypto_price(symbol)
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
    insert_crypto_data()