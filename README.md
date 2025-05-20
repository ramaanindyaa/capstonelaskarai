# 🛍️ Tokopedia Scraper 🔍

Proyek ini berisi skrip Python untuk mengambil (scraping) detail produk dan ulasan dari situs e-commerce Tokopedia, yang diorganisasi berdasarkan kategori produk.

## 📝 Deskripsi Proyek

Scraper ini mengambil informasi produk termasuk nama, harga, deskripsi, spesifikasi, dan ulasan pengguna dari halaman produk Tokopedia. Data disimpan dalam folder berdasarkan kategori dengan file terpisah untuk informasi produk dan ulasannya.

## ⚙️ Persyaratan

- 🐍 Python 3.6+
- 🌐 Browser Chrome
- 📦 Paket Python berikut:
  - 🤖 Selenium
  - 🍲 BeautifulSoup4
  - 🐼 Pandas
  - 🚗 Webdriver-manager

## 🚀 Instalasi

1. Unduh atau clone repositori ini:

   ```bash
   git clone https://github.com/username-anda/capstonelaskarai.git
   cd capstonelaskarai
   ```

2. Instal semua dependensi yang dibutuhkan:

   ```bash
   pip install selenium beautifulsoup4 pandas webdriver-manager
   ```

3. Pastikan browser Chrome sudah terpasang di komputer Anda.

## 🎮 Cara Penggunaan

1. Jalankan skrip:

   ```bash
   python belajar_selenium_tokped.py
   ```

2. Skrip akan:
   - 📋 Menampilkan kategori yang tersedia (Pakaian wanita, Pakaian pria, Alas kaki)
   - 🔄 Mengambil data hingga 3 produk dari setiap kategori
   - 📁 Membuat folder untuk setiap kategori
   - 💾 Menyimpan informasi produk dalam file CSV di dalam folder kategori
   - 💬 Menyimpan ulasan produk dalam file CSV terpisah di folder yang sama

## 📂 Struktur Output

```
/
├── belajar_selenium_tokped.py
├── README.md
├── Pakaian_wanita/
│   ├── Pakaian_wanita.csv
│   ├── Produk1_reviews.csv
│   └── ...
├── Pakaian_pria/
│   ├── Pakaian_pria.csv
│   ├── Produk1_reviews.csv
│   └── ...
└── Alas_kaki/
    ├── Alas_kaki.csv
    ├── Produk1_reviews.csv
    └── ...
```

## ✨ Fitur

- 🪟 Penanganan otomatis untuk popup yang muncul
- ⏱️ Penundaan acak untuk menghindari mekanisme anti-scraping
- 📊 Penyimpanan data terstruktur berdasarkan kategori produk
- 🗣️ Pengumpulan terpisah untuk detail produk dan ulasan pengguna
- 📈 Informasi kemajuan di konsol selama proses scraping

## 🛠️ Kustomisasi

Untuk mengubah URL produk atau menambahkan kategori baru, edit dictionary `categories` di file `belajar_selenium_tokped.py`:

```python
categories = {
    "Nama_Kategori.csv": [
        "url_produk_1",
        "url_produk_2",
        # Tambahkan URL lainnya
    ],
    # Tambahkan kategori lainnya
}
```

Untuk mengubah jumlah maksimal produk yang diambil per kategori, ubah parameter `max_products_per_category` saat memanggil fungsi `scrape_tokopedia_by_category`.

## 🧩 Komponen Utama

1. **🌟 setup_browser()**: Menyiapkan browser Chrome dengan opsi yang sesuai
2. **🚫 close_popup_if_exists()**: Menangani popup yang mungkin muncul
3. **🕵️ scrape_product_details()**: Mengambil informasi detail produk
4. **📝 save_product_to_csv()**: Menyimpan data produk ke file CSV
5. **🗣️ scrape_and_save_reviews()**: Mengambil dan menyimpan ulasan produk
6. **🏆 scrape_tokopedia_by_category()**: Fungsi utama yang mengkoordinasikan proses scraping

## ⚠️ Catatan

Scraper ini dibuat untuk tujuan pembelajaran. Harap perhatikan ketentuan layanan Tokopedia dan robots.txt saat menggunakan alat web scraping. Pertimbangkan untuk menerapkan pembatasan kecepatan yang tepat untuk menghindari beban berlebih pada server mereka.

## 👥 Kontributor

- 🤝 Tim Laskar AI
  - 👨‍💻 Rama Anindya: [GitHub](https://github.com/ramaanindyaa)
  - 👩‍💻 Febhe Maulita May Pramasta: [GitHub](https://github.com/fluffybhe)
  - 👨‍💻 Anak Agung Ngurah Bagus Dwimantara: [GitHub](#)

## 📜 Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT](https://opensource.org/licenses/MIT).
