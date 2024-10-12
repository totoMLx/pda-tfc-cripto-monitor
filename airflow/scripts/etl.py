import pandas as pd
import requests
from datetime import datetime
from utils import get_env_variable, create_db_engine, create_append_to_table
#from dotenv import load_dotenv
#load_dotenv()


def get_crypto_symbols(ninja_key):
    """Obtener todos los simbolos de los criptoactivos desde la API de Ninja"""
    symbols_url = 'https://api.api-ninjas.com/v1/cryptosymbols'
    try:
        response = requests.get(symbols_url, headers={'X-Api-Key': ninja_key})
        response.raise_for_status()  # Lanza excepción si hay error HTTP
        return response.json().get('symbols', [])
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los símbolos: {e}")
        return []

def get_crypto_price(ninja_key, symbol):
    """Obtener el precio actual de cada criptoactivo por símbolo"""
    price_url = f'https://api.api-ninjas.com/v1/cryptoprice?symbol={symbol}'
    try:
        response = requests.get(price_url, headers={'X-Api-Key': ninja_key})
        response.raise_for_status()
        data = response.json()
        return data.get('symbol'), data.get('price')
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio para {symbol}: {e}")
        return symbol, None

def get_dolar_price():
    """Ejemplo de función para obtener el precio del dólar"""
    try:
        response = requests.get("https://dolarapi.com/v1/dolares/blue")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener valor dolar: {e}")
        return None
    

def insert_crypto_data():
    engine = create_db_engine()
    """Insertar precios de criptoactivos en la tabla histórica"""
    ninja_key = get_env_variable('NINJA_API_KEY')
    # Debido a limitaciones en la cantidad de api calls que tenemos, lo restringimos a traernos unicamente el precio de BTC, ETH y DOGE
    # symbols = get_crypto_symbols(ninja_key)
    
    symbols = ['BTCUSDT', 'ETHUSDT', 'DOGEUSDT']
    valor_dolar = get_dolar_price()

    filtered_data = {
    'tipo': valor_dolar['nombre'],
    'compra': valor_dolar['compra'],
    'venta': valor_dolar['venta'],
    'fecha': valor_dolar['fechaActualizacion']
    }
    
    # Convertir el diccionario filtrado en un DataFrame de una fila
    dolar_prices = pd.DataFrame([filtered_data])
    print(dolar_prices)
    create_append_to_table(dolar_prices, 'dolar_prices', engine, '2024_tomas_fernando_campi_schema')

    
    crypto_prices = pd.DataFrame(columns=['symbol', 'price_USD', 'price_pesos', 'date'])
    crypto_prices['symbol'] = symbols

    for row in range(len(crypto_prices)):
        symbol = crypto_prices['symbol'][row]
        symbol_check, price = get_crypto_price(ninja_key, symbol)
        today_date = datetime.now()
        date_str = today_date.strftime('%Y-%m-%d %H:%M:%S')
        
        if symbol_check == symbol:
            print(symbol)
            crypto_prices.at[row, 'price_USD'] = round(float(price), 3)
            crypto_prices.at[row, 'price_pesos'] = round(float(price)*int(filtered_data['venta']),2)
        else:
            crypto_prices.at[row, 'price_USD'] = -1  # Si hay error, precio -1
            crypto_prices.at[row, 'price_pesos'] = -1
            
        crypto_prices.at[row, 'date'] = date_str
    
    create_append_to_table(crypto_prices, 'crypto_prices', engine, '2024_tomas_fernando_campi_schema')


#if __name__ == '__main__':
#    try:
#       engine = create_db_engine()
#        insert_crypto_data(engine)
#    except Exception as e:
#        print(f"Error en la ejecución principal: {e}")