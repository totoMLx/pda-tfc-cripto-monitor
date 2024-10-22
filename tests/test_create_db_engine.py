import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import utils 


class TestCreateDbEngine(unittest.TestCase):

    @patch('utils.create_engine')
    @patch.dict(os.environ, {
    'REDSHIFT_USER': 'user',
    'REDSHIFT_PASSWORD': 'password',
    'REDSHIFT_HOST': 'localhost',
    'REDSHIFT_PORT': '5439',
    'REDSHIFT_DB': 'testdb'
    })  # Simula las variables de entorno
    def test_create_db_engine(self, mock_create_engine):
        """Test que verifica la creación del engine de base de datos."""
        mock_engine = MagicMock(spec=Engine)
        mock_create_engine.return_value = mock_engine

        engine = utils.create_db_engine()
        self.assertEqual(engine, mock_engine)
        mock_create_engine.assert_called_once_with(
            "postgresql://user:password@localhost:5439/testdb"
        )

if __name__ == '__main__':
    unittest.main()