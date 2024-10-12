import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
import sys
import os

# Add the 'scripts' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import utils

class TestCreateDbEngine(unittest.TestCase):
    def setUp(self):
        self.mock_engine = MagicMock(spec=Engine)

    @patch('etl.create_engine')
    @patch('etl.get_env_variable')
    def test_create_db_engine(self, mock_get_env_variable, mock_create_engine):
        mock_get_env_variable.side_effect = ['user', 'pass', 'host', '5439', 'db']
        utils.create_db_engine()
        mock_create_engine.assert_called_once_with("postgresql://user:pass@host:5439/db")

if __name__ == '__main__':
    unittest.main()