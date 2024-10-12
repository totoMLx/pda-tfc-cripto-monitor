import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
import sys
import os

# Añadir el directorio 'scripts' al Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import utils  # Asegúrate de que utils está bien importado

class TestCreateDbEngine(unittest.TestCase):

    def setUp(self):
        self.mock_engine = MagicMock(spec=Engine)

    @patch('utils.create_db_engine', return_value=MagicMock(spec=Engine))  # Cambiado el patch
    @patch('utils.get_env_variable')
    def test_create_db_engine(self, mock_get_env_variable, mock_create_engine):
        # Configurar los valores de retorno del mock de las variables de entorno
        mock_get_env_variable.side_effect = ['user', 'pass', 'host', '5439', 'db']

        # Llamar a la función que queremos probar
        engine = utils.create_db_engine()

        # Verificar que la función `create_engine` fue llamada correctamente
        mock_create_engine.assert_called_once_with("postgresql://user:pass@host:5439/db")

if __name__ == '__main__':
    unittest.main()