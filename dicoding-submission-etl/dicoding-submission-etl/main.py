from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

def main():
    #base URL dari website yang ingin di-scrape
    base_url = 'https://fashion-studio.dicoding.dev/'
    
    #list untuk menyimpan semua data produk dari semua halaman
    all_products = []

    #1. Scrape halaman utama (tanpa /page)
    print(f"Scraping halaman utama: {base_url}")
    try:
        main_page_products = scrape_main(base_url)
        all_products.extend(main_page_products)  #tambahkan hasil ke daftar produk
    except Exception as e:
        print(f"Gagal scrape halaman utama: {e}")

    #2. Scrape halaman dari /page2 sampai /page50
    for page in range(2, 51):
        page_url = f"{base_url}page{page}"
        print(f"Scraping halaman {page}: {page_url}")
        try:
            page_products = scrape_main(page_url)
            all_products.extend(page_products)
        except Exception as e:
            print(f"Gagal scrape halaman {page}: {e}")

    #3. Transformasi data hasil scraping
    print(f"\n Transforming data ({len(all_products)} produk ditemukan)...")
    transformed_df = transform_data(all_products)

    #4. Simpan ke file CSV lokal
    print("Menyimpan data ke CSV...")
    save_to_csv(transformed_df)

    #5. Simpan ke database PostgreSQL (jika koneksi tersedia)
    print("Mengirim data ke PostgreSQL...")
    load_to_postgresql(transformed_df)

    #6. Upload ke Google Sheets
    print("Upload data ke Google Sheets...")
    save_to_google_sheets(
        transformed_df,
        spreadsheet_id='1K392c304gTMv75gM5MRchIX3qiO-0KJQxTNS8czzc-4',
        range_name='Sheet1!A2'
    )

    print("\nSemua proses selesai!")

if __name__ == '__main__':
    main()
