import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
import sys
import os
# Add the 'scripts' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow/scripts'))
# Now you can import your crypto_app module
import crypto_app

class TestCryptoApp(unittest.TestCase):
    def setUp(self):
        """Set up test variables and mocks for each test."""
        self.mock_engine = MagicMock(spec=Engine)

    @patch('crypto_app.create_engine')
    @patch('crypto_app.get_env_variable')
    def test_create_db_engine(self, mock_get_env_variable, mock_create_engine):
        """Test database engine creation."""
        mock_get_env_variable.side_effect = ['user', 'pass', 'host', '5439', 'db']
        crypto_app.create_db_engine()
        mock_create_engine.assert_called_once_with("postgresql://user:pass@host:5439/db")

    @patch('crypto_app.requests.get')
    def test_get_crypto_symbols(self, mock_get):
        """Test fetching cryptocurrency symbols from API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'symbols': ['BTC', 'ETH']}
        mock_get.return_value = mock_response
        symbols = crypto_app.get_crypto_symbols('dummy_key')
        self.assertEqual(symbols, ['BTC', 'ETH'])
        mock_get.assert_called_with('https://api.api-ninjas.com/v1/cryptosymbols', headers={'X-Api-Key': 'dummy_key'})

    @patch('crypto_app.requests.get')
    def test_get_crypto_price(self, mock_get):
        """Test fetching cryptocurrency price from API."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'symbol': 'BTC', 'price': '50000'}
        mock_get.return_value = mock_response
        symbol, price = crypto_app.get_crypto_price('dummy_key', 'BTC')
        self.assertEqual((symbol, price), ('BTC', '50000'))
        mock_get.assert_called_with('https://api.api-ninjas.com/v1/cryptoprice?symbol=BTC', headers={'X-Api-Key': 'dummy_key'})

    @patch('pandas.DataFrame.to_sql')
    def test_insert_crypto_data(self, mock_to_sql):
        """Test insertion of cryptocurrency data into the database."""
        crypto_app.insert_crypto_data(self.mock_engine)
        mock_to_sql.assert_called()

if __name__ == '__main__':
    unittest.main()