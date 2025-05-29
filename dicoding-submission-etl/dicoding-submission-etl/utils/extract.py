import requests
from bs4 import BeautifulSoup

def scrape_main(url):
    """
    Fungsi untuk mengambil data produk dari sebuah halaman web.
    Data yang diambil mencakup: title, price, rating, colors, size, dan gender.
    """

    #1. Mengirim permintaan HTTP ke URL
    try:
        response = requests.get(url, timeout=10) #timeout 10 detik
        response.raise_for_status() #cek jika status bukan 200 (OK), akan lempar error
    except requests.exceptions.RequestException as e:
        raise Exception(f"Gagal mengakses URL: {url}. Detail: {e}")

    #2. Mem-parse HTML menggunakan BeautifulSoup
    try:
        soup = BeautifulSoup(response.text, 'html.parser') #parsing HTML
        products = [] #list untuk menampung semua data produk

        #3. Cari semua elemen <div> yang merupakan kartu produk
        product_cards = soup.find_all('div', class_='collection-card')

        for card in product_cards:
            #ambil judul produk
            title_element = card.find('h3', class_='product-title')
            title = title_element.text.strip() if title_element else 'Unknown Title'

            #ambil harga produk
            price_element = card.find('div', class_='price-container')
            price = price_element.text.strip() if price_element else 'Price Unvailable'

            #ambil rating produk
            rating_element = card.find('p', string=lambda text: text and 'Rating' in text)
            rating = rating_element.text.strip() if rating_element else 'No Rating'

            #ambil informasi warna
            colors_element = card.find('p', string=lambda text: text and 'Colors' in text)
            colors = colors_element.text.strip() if colors_element else 'No Colors Info'

            #ambil ukuran produk
            size_element = card.find('p', string=lambda text: text and 'Size' in text)
            size = size_element.text.strip() if size_element else 'No Size Info'

            #ambil informasi gender
            gender_element = card.find('p', string=lambda text: text and 'Gender' in text)
            gender = gender_element.text.strip() if gender_element else 'No Gender Info'

            #simpan semua data produk ke dalam dictionary
            product_info = {
                'title': title,
                'price': price,
                'rating': rating,
                'colors': colors,
                'size': size,
                'gender': gender
            }

            #tambahkan ke list produk 
            products.append(product_info)
        
        #4. Kembalikan semua produk yang ditemukan
        return products 

    except Exception as e:
        raise Exception(f"Gagal melakukan parsing HTML. Detail: {e}")