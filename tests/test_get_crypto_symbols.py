import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the 'scripts' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import etl

class TestGetCryptoSymbols(unittest.TestCase):
    @patch('etl.requests.get')
    def test_get_crypto_symbols(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'symbols': ['BTC', 'ETH']}
        mock_get.return_value = mock_response
        symbols = etl.get_crypto_symbols('dummy_key')
        self.assertEqual(symbols, ['BTC', 'ETH'])
        mock_get.assert_called_with('https://api.api-ninjas.com/v1/cryptosymbols', headers={'X-Api-Key': 'dummy_key'})

if __name__ == '__main__':
    unittest.main()