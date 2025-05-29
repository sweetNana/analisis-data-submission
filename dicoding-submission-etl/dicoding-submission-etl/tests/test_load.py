import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets

class TestLoad(unittest.TestCase):
    """
    Unit test untuk fungsi-fungsi load di modul utils.load
    """

    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv_success(self, mock_to_csv):
        """
        Test bahwa fungsi save_to_csv memanggil DataFrame.to_csv dengan benar.
        """
        #data dummy untuk pengujian
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [10000, 20000],
            'rating': [4.5, 5.0]
        })

        #jalankan fungsi
        save_to_csv(df, 'test.csv')

        #pastikan fungsi to_csv dipanggil dengan parameter yang tepat
        mock_to_csv.assert_called_once_with('test.csv', index=False)

    @patch('utils.load.build')  #mock fungsi build() dari Google API client
    @patch('utils.load.Credentials.from_service_account_file')  #mock pemanggilan kredensial
    def test_save_to_google_sheets_success(self, mock_creds, mock_build):
        """
        Test bahwa fungsi save_to_google_sheets memanggil API Google Sheets dengan benar.
        """
        #data dummy untuk pengujian
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [10000, 20000],
            'rating': [4.5, 5.0]
        })

        #siapkan mock credentials dan mock service dari Google API
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        #jalankan fungsi
        save_to_google_sheets(df, 'spreadsheet_id_dummy', 'Sheet1!A2')

        #verifikasi bahwa metode update pada Google Sheets API dipanggil
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

#menjalankan semua test ketika file ini dijalankan secara langsung
if __name__ == '__main__':
    unittest.main()
