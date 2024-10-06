import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the 'scripts' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
import crypto_app

class TestGetCryptoPrice(unittest.TestCase):
    @patch('crypto_app.requests.get')
    def test_get_crypto_price(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'symbol': 'BTC', 'price': '50000'}
        mock_get.return_value = mock_response
        symbol, price = crypto_app.get_crypto_price('dummy_key', 'BTC')
        self.assertEqual((symbol, price), ('BTC', '50000'))
        mock_get.assert_called_with('https://api.api-ninjas.com/v1/cryptoprice?symbol=BTC', headers={'X-Api-Key': 'dummy_key'})

if __name__ == '__main__':
    unittest.main()