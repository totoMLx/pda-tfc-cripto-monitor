import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the 'scripts' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import crypto_app

class TestInsertCryptoData(unittest.TestCase):
    def setUp(self):
        self.mock_engine = MagicMock()

    @patch('pandas.DataFrame.to_sql')
    def test_insert_crypto_data(self, mock_to_sql):
        crypto_app.insert_crypto_data(self.mock_engine)
        mock_to_sql.assert_called()

if __name__ == '__main__':
    unittest.main()