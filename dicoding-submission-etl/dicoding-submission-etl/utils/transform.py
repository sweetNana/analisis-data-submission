import pandas as pd 
import numpy as np 
from datetime import datetime
import warnings

#mengabaikan peringatan FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

#mengaktifkan opsi eksplisit untuk penyesuaian tipe data di masa depan
pd.set_option('future.no_silent_downcasting', True)

def transform_data(products):
    """
    Fungsi untuk membersihkan dan memproses data hasil scraping menjadi DataFrame yang rapi.
    """

    #1. Ubah list of dict menjadi DataFrame
    df = pd.DataFrame(products)

    #2. Buang baris yang memiliki judul produk tidak valid
    df = df[df['title'].str.lower() != 'unknown product']

    #3. Bersihkan kolom harga
    #   - hapus simbol selain angka dan titik
    #   - ganti string kosong dengan NaN 
    #   - drop baris yang tidak punya harga
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True)
    df['price'] = df['price'].replace('', np.nan)
    df.dropna(subset=['price'], inplace=True)

    #4. Konversi harga ke float dan ubah ke dalam mata uang Rupiah (asumsi: kurs USD ke IDR = 16000)
    df['price'] = df['price'].astype(float)*16000

    #5. Bersihkan kolom rating
    df['rating'] = df['rating'].replace(r'[^0-9]', '', regex=True)
    df['rating'] = df['rating'].replace('', np.nan)
    df.dropna(subset=['rating'], inplace=True)
    df['rating'] = df['rating'].astype(float)

    #6. Bersihkan kolom colors (ambil hanya angka banyaknya warna)
    df['colors'] = df['colors'].replace(r'\D', '', regex=True)
    df['colors'] = df['colors'].replace('', np.nan)
    df.dropna(subset=['colors'], inplace=True)
    df['colors'] = df['colors'].astype(int)

    #7. Bersihkan kolom size dan gender dari awalan seperti "Size:" atau "Gender:"
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True)
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True)

    #8. Hapus baris duplikat dan yang masih mengandung nilai kosong
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    #9. Tambahkan kolom timestamp (waktu transformasi dilakukan)
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #10. Kembalikan DataFrame yang sudah dibersihkan dan diproses
    return df 