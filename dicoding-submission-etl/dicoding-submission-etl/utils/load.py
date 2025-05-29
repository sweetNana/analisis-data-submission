import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

#----------------------------------------------#
# FUNGSI UNTUK MENYIMPAN DATA KE FILE CSV
#----------------------------------------------#
def save_to_csv(df, filename="products.csv"):
    """
    Menyimpan DataFrame ke file CSV lokal.

    Args:
        df (DatFrame): Data hasil transformasi.
        filename (str): Nama file CSV (default: products.csv)
    """
    df.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke file CSV: {filename}")

#---------------------------------------------------#
# FUNGSI UNTUK MENYIMPAN DATA KE GOOGLE SPREADSHEETS
#---------------------------------------------------#
def save_to_google_sheets(df, spreadsheet_id, range_name):
    """
    Mengirim DataFrame ke Goole Sheets.

    Args:
        df (DatFrame): Data hasil transformasi.
        spreadsheet_id (srt): ID spreadsheet dari Google Sheets.
        range_name (str): Range penempatan data di spreadsheet ('Sheet1!A1').
    """
    try:
        #autentikasi ke Google Sheets API untuk menggunakan file JSON credential
        creds = Credentials.from_service_account_file('./google-sheets-api-dicoding.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        #ubah DataFrame menjadi list of lists
        values = df.values.tolist()

        #buat payload untuk dikirim
        body = {
            'values': values
        }

        #kirim data ke Google Sheets menggunakan metode update
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW', #data tidak diformat secara otomatis
            body=body
        ).execute()

        print("Data berhasil dikirim ke Google Sheets.")

    except Exception as e:
        print(f"Gagal menyimpan ke Google Sheets: {e}")

#---------------------------------------------------#
# FUNGSI UNTUK MENYIMPAN DATA KE POSTRESQL
#---------------------------------------------------#
def load_to_postgresql(df, table_name='products'):
    """
    Menyimpan DataFrame ke database PostgreSQL.

    Args:
        df (DataFrame): Data hasil transformasi.
        table_name (str): Nama tabel tujuan di PostgreSQL.
    """
    try:
        #konfigurasi koneksi ke PostgreSQL
        username = 'nanad'
        password = 'nanad'
        host = 'localhost'
        port = '5432'
        database = 'dicoding_etl'

        #buat koneksi database menggunakan SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        #simpan data ke dalam tabel PostgreSQL
        #if_exists='replace' artinya tabel lama akan dihapus jika sudah ada
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e: 
        print(f"Gagal menyimpan ke PostreSQL: {e}")
