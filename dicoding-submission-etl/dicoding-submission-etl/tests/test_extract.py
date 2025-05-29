import unittest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_main
import requests 

class TestExtract(unittest.TestCase):
    """
    Unit test untuk menguji fungsi scrape_main dari modul utils.extract
    """

    @patch('utils.extract.requests.get')
    def test_scrape_main_success(self, mock_get):
        """
        Test jika scrape_main berhasil mengambil dan memproses data produk dari HTML yang valid.
        """
        #URL target 
        url = "https://fashion-studio.dicoding.dev/"

        #mock response dengan HTML yang mengandung 1 produk
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Rating: 5 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: M, L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response #gantikan requests.get dengan mock

        #jalankan fungsi
        result = scrape_main(url)

        #assertion: memastikan hasilnya sesuai harapan
        self.assertIsInstance(result, list) #hasil harus berupa list
        self.assertGreater(len(result), 0) #list tidak boleh kosong
        self.assertIn('title', result[0]) #harus ada field 'title' pada data produk
        self.assertEqual(result[0]['title'], 'Test Product') #nama produk harus sesuai mock

    @patch('utils.extract.requests.get')
    def test_scrape_main_failure(self, mock_get):
        """
        Test jika scrape_main gagal saat requests.get mengembalikan error (misalnya 404).
        """
        #URL 
        url = "https://fashion-studio.dicoding.dev/"

        #mock response error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = mock_response

        #jalankan fungsi dan pastikan raise Exception
        with self.assertRaises(Exception) as context:
            scrape_main(url)

        #cek apakah pesan error sesuai ekspektasi
        self.assertIn('404', str(context.exception))  #pastikan ada "404" di pesan error

#menjalankan unit test saat file ini dijalankan langsung
if __name__ == '__main__':
    unittest.main()

