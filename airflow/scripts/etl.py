import pandas as pd
from datetime import datetime
from utils import get_env_variable, create_db_engine, create_append_to_table, get_crypto_data, get_dolar_price, get_crypto_price
from config import crypto_ids


def extract_crypto_data():
    
    """Insertar precios de criptoactivos en la tabla histórica"""
    ninja_key = get_env_variable('NINJA_API_KEY')
    
    valor_dolar = get_dolar_price()

    filtered_data = {
    'tipo': valor_dolar['nombre'],
    'compra': valor_dolar['compra'],
    'venta': valor_dolar['venta'],
    'fecha': valor_dolar['fechaActualizacion']
    }
    
    dolar_prices = pd.DataFrame([filtered_data])
    ## Guardar el DataFrame en formato Parquet para levantarlo despues en el transform
    dolar_prices.to_parquet('/opt/airflow/data/dolar_prices.parquet', index=False, engine='pyarrow')
    print('Dolar prices saved to parquet')
    
    ## Extraemos precios de las criptos
    crypto_prices = pd.DataFrame(columns=['symbol','crypto_id', 'price_USD', 'date'])
    symbolsusdt = [symbol+'USDT' for symbol in crypto_ids]
    crypto_prices['symbol'] = symbolsusdt
    crypto_prices['crypto_id'] = list(crypto_ids.values())
    today_date = datetime.now()
    date_str = today_date.strftime('%Y-%m-%d %H:%M:%S')

    for row in range(len(crypto_prices)):
        symbol = crypto_prices['symbol'][row]
        symbol_check, price = get_crypto_price(ninja_key, symbol)
        
        if symbol_check == symbol:
            crypto_prices.at[row, 'price_USD'] = round(float(price), 3)
        else:
            crypto_prices.at[row, 'price_USD'] = -1  # Si hay error, precio -1
            
        crypto_prices.at[row, 'date'] = date_str
        
    ## Guardamos como parquet para levantarlo despues en el transform
    crypto_prices.to_parquet('/opt/airflow/data/crypto_prices.parquet', index=False, engine='pyarrow')
    print('Crypto prices saved to parquet')
    
    ## Extraemos data de las 3 cryptos
    cmc_key = get_env_variable('CMC_API_KEY')
    crypto_data = pd.DataFrame(columns=['id','symbol','date','market_cap','cmc_dominance', 'cmc_rank', 'is_fiat'])
    crypto_data['id'] = list(crypto_ids.values())
    crypto_data['symbol'] = list(crypto_ids.keys())
    
    for row in range(len(crypto_data)):
        id = crypto_data['id'][row]
        data = get_crypto_data(cmc_key, id)
        
        market_cap = data['data'][id]['quote']['USD']['market_cap']
        cmc_dominance = data['data'][id]['quote']['USD']['market_cap_dominance']
        cmc_rank = data['data'][id]['cmc_rank']
        is_fiat = data['data'][id]['is_fiat']
        
        crypto_data.at[row, 'market_cap'] = market_cap
        crypto_data.at[row, 'cmc_dominance'] = cmc_dominance
        crypto_data.at[row, 'cmc_rank'] = cmc_rank
        crypto_data.at[row, 'is_fiat'] = is_fiat
        crypto_data.at[row, 'date'] = date_str
        
    ## Guardamos como parquet para levantarlo despues en el transform
    crypto_data.to_parquet('/opt/airflow/data/crypto_data.parquet', index=False, engine='pyarrow')    
    print('Crypto data saved to parquet')
   


def transform_load_crypto_data():
    engine = create_db_engine()
    
    # transform and load dolar data
    dolar_prices = pd.read_parquet('/opt/airflow/data/dolar_prices.parquet')
    create_append_to_table(dolar_prices, 'bt_dolar_prices', engine, '2024_tomas_fernando_campi_schema')
    print('Dolar prices sent to DB')
    
    # transform and load crypto prices
    crypto_prices = pd.read_parquet('/opt/airflow/data/crypto_prices.parquet')
    valor_dolar = dolar_prices['venta'][0]
    crypto_prices['price_pesos'] = crypto_prices['price_USD']*int(valor_dolar)
    create_append_to_table(crypto_prices, 'bt_crypto_prices', engine, '2024_tomas_fernando_campi_schema')
    print('Crypto prices sent to DB')
    
    # transform and load crypto data
    crypto_data = pd.read_parquet('/opt/airflow/data/crypto_data.parquet')   
    create_append_to_table(crypto_data, 'lk_crypto_data', engine, '2024_tomas_fernando_campi_schema')
    print('Crypto data sent to DB')


def create_update_dm_crypto_table():
    engine = create_db_engine()

    query = """
    CREATE TABLE dm_crypto_daily_information as
    with stg as(
    select
        row_number() over(partition by cp.crypto_id order by cp.date DESC) as rank,
        cp.crypto_id,
        cd.symbol,
        cp.price_usd,
        cp.price_pesos,
        cd.market_cap,
        cd.cmc_dominance,
        cd.cmc_rank,
        cd.is_fiat AS fiat_flag,
        cp.date AS update_date
    FROM "2024_tomas_fernando_campi_schema".bt_crypto_prices cp
    LEFT JOIN "2024_tomas_fernando_campi_schema".lk_crypto_data cd ON cd.id = cp.crypto_id and cast(cd.date as date) = cast(cp.date as date)
    )
    select 
    *
    from stg 
    where rank=1
    order by cmc_rank asc;
    """
    
    connection = engine.connect()
    connection.execute("DROP TABLE IF EXISTS dm_crypto_daily_information")
    print('Table dm_crypto_daily_information dropped')
    connection.execute(query) #Crecion de tabla data mart con info del dia de las criptos 
    print('Table dm_crypto_daily_information created successfuly')