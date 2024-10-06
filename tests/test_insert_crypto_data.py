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

    @patch('crypto_app.get_crypto_symbols', return_value=['BTC', 'ETH'])  # Mock API response for symbols
    @patch('crypto_app.get_crypto_price', side_effect=[('BTC', 50000.0), ('ETH', 4000.0)])  # Mock API price data
    @patch.dict('os.environ', {'NINJA_API_KEY': 'fake_api_key'})  # Mock environment variable
    @patch('pandas.DataFrame.to_sql')  # Mock the to_sql method to avoid actual DB operations
    def test_insert_crypto_data(self, mock_to_sql, mock_get_price, mock_get_symbols):
        # Run the function
        crypto_app.insert_crypto_data(self.mock_engine)
        
        # Check if the to_sql method was called
        mock_to_sql.assert_called()  # This will ensure the to_sql method is called
        
        # You can also assert the number of times it's called, if you expect a specific number of calls
        self.assertEqual(mock_to_sql.call_count, 1)

if __name__ == '__main__':
    unittest.main()