import os
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
    try:
        user = quote_plus(get_env_variable('REDSHIFT_USER'))
        password = quote_plus(get_env_variable('REDSHIFT_PASSWORD'))
        host = get_env_variable('REDSHIFT_HOST')
        port = get_env_variable('REDSHIFT_PORT')
        database = get_env_variable('REDSHIFT_DB')
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(connection_string)
    except Exception as e:
        raise ConnectionError(f"Error creando la conexión con Redshift: {e}")
    
    
def create_append_to_table(df, name, engine, schema):
    """Insertar o añadir datos a la tabla SQL"""
    try:
        df.to_sql(name=name, con=engine, schema=schema, if_exists='append', index=False)
    except Exception as e:
        print(f"Error al insertar los datos en la tabla {name}: {e}")