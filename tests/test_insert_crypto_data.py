import unittest
from unittest.mock import patch, MagicMock
import os
import etl  # Asegúrate de importar tu módulo etl

class TestInsertCryptoData(unittest.TestCase):

    def setUp(self):
        self.mock_engine = MagicMock()

    @patch('etl.create_append_to_table')  # Mockear operaciones SQL
    @patch('etl.create_db_engine', return_value=MagicMock())  # Mockear creación del engine
    @patch('etl.get_crypto_price', side_effect=[('BTCUSDT', 50000.0), ('ETHUSDT', 4000.0), ('DOGEUSDT', 0.05)])  # Mock precios
    @patch('etl.get_dolar_price', return_value={
        'nombre': 'Blue',
        'compra': 1100,
        'venta': 1180,
        'fechaActualizacion': '2024-10-12T18:44:25.936874+00:00'
    })  # Mock valor dólar
    @patch.dict(os.environ, {'NINJA_API_KEY': 'fake_api_key'})  # Mock variables de entorno
    def test_insert_crypto_data(self, mock_get_dolar, mock_get_crypto, mock_create_engine, mock_append_to_table):
        # Ejecutar la función que queremos probar
        etl.insert_crypto_data()

        # Verificar que las funciones mockeadas se llamaron correctamente
        mock_create_engine.assert_called_once()  # Verifica que se creó el engine
        self.assertEqual(mock_get_crypto.call_count, 3)  # Verifica que se llamaron los precios de 3 criptos
        mock_append_to_table.assert_called()  # Verifica que los datos se guardaron en la DB

if __name__ == '__main__':
    unittest.main()