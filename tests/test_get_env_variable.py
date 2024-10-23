import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
import sys
import os

# Añadir el directorio 'scripts' al Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import utils

class TestGetEnvVariable(unittest.TestCase):

    @patch.dict(os.environ, {
        'REDSHIFT_USER': 'user',
        'REDSHIFT_PASSWORD': 'password'
    })
    def test_get_env_variable(self):
        """Test que verifica la obtención de variables de entorno."""
        self.assertEqual(utils.get_env_variable('REDSHIFT_USER'), 'user')
        self.assertEqual(utils.get_env_variable('REDSHIFT_PASSWORD'), 'password')

        with self.assertRaises(EnvironmentError):
            utils.get_env_variable('NON_EXISTENT_VAR')

if __name__ == '__main__':
    unittest.main()