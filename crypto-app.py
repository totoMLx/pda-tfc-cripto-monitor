import pandas as pd
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

ninja_key = os.getenv('NINJA_API_KEY')

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

symbols = get_crypto_symbols()

crypto_prices = pd.DataFrame(columns=['symbol', 'price_USD', 'date'])
crypto_prices['symbol'] = symbols

for row in range(len(crypto_prices)):
    symbol = crypto_prices['symbol'][row]
    symbol_check,price = get_crypto_price(symbol)
    current_date = datetime.now().date()
    if symbol_check == symbol:
        crypto_prices.at[row,'price_USD'] = float(price)
        crypto_prices.at[row, 'date'] = current_date
    else:
        crypto_prices.at[row,'price'] = -1
        crypto_prices.at[row, 'date'] = current_date
        
crypto_prices['price_truc_USD'] = round(crypto_prices['price_USD'])
