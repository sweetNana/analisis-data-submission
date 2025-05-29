import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    """
    Unit test untuk menguji fungsi transform_data dari modul utils.transform
    """

    def test_transform_data_success(self):
        """
        Test jika transform_data berhasil memproses list produk valid menjadi DataFrame
        dengan kolom-kolom yang diharapkan.
        """
        #data dummy: produk dengan nilai valid
        products = [
            {'title': 'Product 1', 'price': '10000', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'},
            {'title': 'Product 2', 'price': '20000', 'rating': '5.0', 'colors': '3', 'size': 'L', 'gender': 'Women'}
        ]
        
        #jalankan fungsi transform
        df = transform_data(products)
        
        #pastikan DataFrame terbentuk dengan 2 baris
        self.assertEqual(len(df), 2)

        #pastikan kolom penting tersedia
        self.assertIn('price', df.columns)
        self.assertIn('rating', df.columns)
        self.assertIn('timestamp', df.columns)

        #pastikan nilai price dan rating valid (angka positif)
        self.assertTrue(df['price'].iloc[0] > 0)
        self.assertTrue(df['rating'].iloc[0] > 0)

    def test_transform_data_invalid_price(self):
        """
        Test jika produk dengan harga tidak valid (bukan angka) dibuang/dilewatkan.
        """
        #data dummy: price tidak valid (string)
        products = [
            {'title': 'Product 1', 'price': 'invalid_price', 'rating': '4.5', 'colors': '3', 'size': 'M', 'gender': 'Men'}
        ]
        
        #jalankan transformasi
        df = transform_data(products)
        
        #pastikan baris dengan price tidak valid tidak masuk ke DataFrame
        self.assertEqual(len(df), 0)

#menjalankan unit test saat file ini dijalankan langsung
if __name__ == '__main__':
    unittest.main()
