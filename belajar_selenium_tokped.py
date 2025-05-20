from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import random
import os
import pandas as pd

# Definisi kategori dan URL
categories = {
    "Pakaian_wanita.csv": [
        "https://www.tokopedia.com/istana-fashion11/april-top-atasan-wanita-korean-top-baju-knit-basic-long-sleeve-april-top-panjang-kemeja-bona-viral-1730393737063335819",
        "https://www.tokopedia.com/orloid-883/september-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-pendek-basic-short-sleeve-1729580958718460989",
        "https://www.tokopedia.com/firda-fashion-862/dress-kaftan-batik-elegan-wanita-pesta-aruna-1729615492746545673"
    ],
    "Pakaian_pria.csv": [
        "https://www.tokopedia.com/novoidminds/no-void-minds-aezy-regular-fit-core-t-shirt-charcoal-charcoal-s-59ab9",
        "https://www.tokopedia.com/cozyclub/cozyclub-frank-polo-knit-shirt-kaos-kerah-pria-kaos-lengan-pendek-baju-brown-panjang-casual-1729625526336981441"
    ],
    "Alas_kaki.csv": [
        "https://www.tokopedia.com/pinkeyofficial/pinkey-p026-sepatu-boots-wanita-flat-korea-premium-quality-cream-36",
        "https://www.tokopedia.com/pose-shoes-idn/poseshoes-live-streaming-pose-cloud-bounce-cat-paw-sandal-anti-selip-nyaman-anti-bau-bagian-bawah-lembut-dalam-di-luar-ruangan-pria-dan-wanita-pasangan-rumah-serbaguna-beraneka-warna-kualitas-2024-musim-panas-gaya-panas-shoes-p68101-1730807813095786110"
    ]
    # Tambahkan kategori lain sesuai kebutuhan
}

def setup_browser():
    """Setup dan mengembalikan instance browser Chrome"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })
    return webdriver.Chrome(options=chrome_options)

def close_popup_if_exists(driver, timeout=5):
    """Menutup popup jika muncul"""
    try:
        popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[role="dialog"]'))
        )
        print("Popup detected")
        close_button = popup.find_element(By.CSS_SELECTOR, 'button')
        close_button.click()
        print("Popup closed")
        sleep(1)
    except TimeoutException:
        print("No popup appeared")

def scrape_product_details(browser, url, category_file):
    """
    Scrape detail produk dari URL yang diberikan
    dan menyimpannya ke file CSV berdasarkan kategori
    """
    print(f"\n{'='*50}")
    print(f"🔍 Scraping: {url}")
    print(f"📁 Category: {category_file}")
    print(f"{'='*50}\n")
    
    browser.get(url)
    close_popup_if_exists(browser)
    
    try:
        print("Waiting for product detail to load...")
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-j63za0"))
        )
        print("✅ Page is ready!")
        sleep(3)  # Allow full JS to load

        html = browser.execute_script("return document.documentElement.innerHTML")
        soup = BeautifulSoup(html, "html.parser")

        # === Detect Product Name ===
        product_name_tag = soup.find("h1", class_="css-j63za0")
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else None
        if not product_name:
            product_name_tag = soup.find("h1", class_="css-14yroid")
            product_name = product_name_tag.get_text(strip=True) if product_name_tag else None
        
        if product_name:
            print(f"🔹 Product Name Detected: {product_name}")
        else:
            print("❌ Product name not found.")
            return False

        # === Get Product Prices ===
        current_price_tag = soup.find("div", {"data-testid": "lblPDPDetailProductPrice"})
        original_price_tag = soup.find("span", {"data-testid": "lblPDPDetailOriginalPrice"})

        current_price = current_price_tag.get_text(strip=True) if current_price_tag else "-"
        original_price = original_price_tag.get_text(strip=True) if original_price_tag else "-"

        print(f"💰 Current Price : {current_price}")
        print(f"💸 Original Price: {original_price}")

        # === Get Product Image URL ===
        image_tag = soup.find("img", {"data-testid": "PDPMainImage"})
        image_url = image_tag["src"] if image_tag and image_tag.has_attr("src") else "-"
        print(f"🖼️ Image URL     : {image_url}")

        # === Get Stock Quantity ===
        stock_tag = soup.find("p", {"data-testid": "stock-label"})
        stock_value = "-"
        if stock_tag:
            bold_tag = stock_tag.find("b")
            if bold_tag:
                stock_value = bold_tag.get_text(strip=True)

        print(f"📦 Stock        : {stock_value}")

        # Prepare product data
        product_data = {
            "Product Name": product_name or "-",
            "Current Price": current_price,
            "Original Price": original_price,
            "Image URL": image_url,
            "Stock": stock_value
        }

        # Save to CSV file
        save_product_to_csv(product_data, category_file)
        
        # Collect reviews (kirimkan category_file juga)
        scrape_and_save_reviews(browser, product_name, category_file)
        
        return True
        
    except TimeoutException:
        print("❌ Page load timeout!")
        return False
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return False

def save_product_to_csv(product_data, filename):
    """Menyimpan data produk ke file CSV dalam folder kategori"""
    # Buat nama folder dari nama file (hilangkan ekstensi .csv)
    folder_name = os.path.splitext(filename)[0]
    
    # Buat path folder
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Buat folder jika belum ada
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Created new directory: {folder_name}/")
    
    # Tentukan path file dalam folder
    file_path = os.path.join(folder_path, filename)
    
    # Proses seperti sebelumnya, tapi dengan path file yang baru
    if os.path.exists(file_path):
        # Read existing CSV to count rows
        existing_df = pd.read_csv(file_path)
        existing_rows = len(existing_df)

        # New item_id is next number
        item_id = existing_rows + 1
        product_data['item_id'] = item_id

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Append without header
        df.to_csv(file_path, mode='a', index=False, header=False)
        print(f"💾 Appended product info as item_id {item_id} to existing file: {folder_name}/{filename}")

    else:
        # First entry, item_id = 1
        product_data['item_id'] = 1

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Write new file with header
        df.to_csv(file_path, index=False)
        print(f"💾 Created new file and saved product info as item_id 1: {folder_name}/{filename}")

def scrape_and_save_reviews(browser, product_name, category_file):
    """Scrape dan menyimpan review produk dalam folder kategori"""
    try:
        print("🧭 Scrolling to review section...")
        sleep(2)

        # scrolling down slowly
        stopScrolling = 0
        while True:
            stopScrolling += 1
            browser.execute_script("window.scrollBy(0,40)")
            sleep(0.5)
            if stopScrolling > 120:
                break
        sleep(3)
    except Exception as e:
        print(f"⚠️ Couldn't scroll to review section: {e}")
        return

    all_reviews = []
    page_number = 1

    while True:
        print(f"\n📖 Scraping review page {page_number}...\n")

        # Scroll to Reviews Section
        try:
            review_container = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "review-feed"))
            )
            browser.execute_script("arguments[0].scrollIntoView();", review_container)
            sleep(2)
        except:
            print("⚠️ Review section not found or not visible yet.")
            break

        # Refresh soup after scroll
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find All Reviews
        review_articles = soup.find_all("article", class_="css-15m2bcr")
        for idx, article in enumerate(review_articles, 1):
            review_text_tag = article.find("span", {"data-testid": "lblItemUlasan"})
            review_text = review_text_tag.get_text(strip=True) if review_text_tag else None

            rating_tag = article.find("div", {"data-testid": "icnStarRating"})
            rating = rating_tag.get("aria-label") if rating_tag else None

            date_tag = article.find("p", string=lambda text: text and any(k in text for k in ["minggu", "hari", "bulan"]))
            review_date = date_tag.get_text(strip=True) if date_tag else None

            if review_text or rating or review_date:
                print(f"💬 Review #{len(all_reviews)+1}:")
                print(f"   📌 Text   : {review_text if review_text else '-'}")
                print(f"   ⭐ Rating : {rating if rating else '-'}")
                print(f"   🕒 Date   : {review_date if review_date else '-'}")
                all_reviews.append({
                    "review": review_text,
                    "rating": rating,
                    "date": review_date
                })
            else:
                print(f"💬 Review #{len(all_reviews)+1}: No content found.")

        # Try to Click Next Button
        try:
            next_button = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Laman berikutnya') and not(@disabled)]"))
            )
            print("➡️ Moving to next page...")
            next_button.click()
            page_number += 1
            sleep(3)  # Wait before scraping next page
        except (TimeoutException, NoSuchElementException):
            print("✅ Reached last page or next button is not clickable.")
            break

    # Save reviews to CSV
    if all_reviews:
        print(f"✅ Total reviews collected: {len(all_reviews)}")
        df = pd.DataFrame(all_reviews)
        
        # Hilangkan karakter yang tidak valid untuk nama file di Windows
        safe_product_name = product_name[:50]
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            safe_product_name = safe_product_name.replace(char, '_')
        
        # Buat nama folder dari nama file kategori (hilangkan ekstensi .csv)
        folder_name = os.path.splitext(category_file)[0]
        folder_path = os.path.join(os.getcwd(), folder_name)
        
        # Pastikan folder sudah ada (seharusnya sudah dibuat saat menyimpan produk)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # Set path file review di dalam folder kategori
        filename = f"{safe_product_name}_reviews.csv"
        file_path = os.path.join(folder_path, filename)
        
        df.to_csv(file_path, index=False)
        print(f"💾 Reviews saved to: {folder_name}/{filename}")
    else:
        print("⚠️ No reviews collected.")

def scrape_tokopedia_by_category(categories_dict, max_products_per_category=5):
    """
    Menjalankan scraper untuk setiap kategori dan URLnya
    
    Args:
        categories_dict: Dictionary dengan key=nama file kategori dan value=list URL
        max_products_per_category: Maksimal produk yang discrape per kategori
    """
    browser = setup_browser()
    
    try:
        for category_file, urls in categories_dict.items():
            print(f"\n\n{'*'*70}")
            print(f"📂 PROCESSING CATEGORY: {category_file}")
            print(f"{'*'*70}\n")
            
            # Batasi jumlah produk per kategori
            product_count = 0
            for url in urls:
                if product_count >= max_products_per_category:
                    break
                
                success = scrape_product_details(browser, url, category_file)
                if success:
                    product_count += 1
                
                # Tambahkan jeda untuk menghindari anti-scraping
                sleep_time = random.uniform(2, 5)
                print(f"⏲️ Waiting for {sleep_time:.1f} seconds before next product...")
                sleep(sleep_time)
                
            print(f"\n✅ Completed scraping {product_count} products for category: {category_file}")
    
    finally:
        print("\n🏁 All scraping tasks completed!")
        browser.quit()

if __name__ == "__main__":
    # Informasi tentang kategori yang tersedia
    print("""
    🛍️ TOKOPEDIA SCRAPER 🛍️
    
    Kategori yang tersedia:
    1. Pakaian wanita
    2. Pakaian pria
    3. Alas kaki
    """)
    
    # Jalankan scraper dengan batasan 3 produk per kategori
    scrape_tokopedia_by_category(categories, max_products_per_category=3)


