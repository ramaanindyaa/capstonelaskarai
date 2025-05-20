from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
import random
import os
import pandas as pd

'''
Kategori:
1. Pakaian wanita
2. Pakaian pria
3. Alas kaki
4. Aksesoris
5. Produk kecantikan
6. Elektronik
7. Kesehatan
8. Bayi dan anak
'''

category = "Pakaian_pria.csv"

def close_popup_if_exists(driver, timeout=5):
    try:
        # Tunggu hingga elemen pop-up muncul (gunakan role dialog atau class unik jika ada)
        popup = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[role="dialog"]'))
        )
        print("Popup detected")

        # Coba cari tombol tutup (biasanya berupa <button> atau <svg> di dalam button)
        close_button = popup.find_element(By.CSS_SELECTOR, 'button')
        close_button.click()
        print("Popup closed")

        # Tunggu sedikit untuk memastikan popup tertutup
        sleep(1)
    except TimeoutException:
        print("No popup appeared")

# === Setup Edge Options ===
edge_options = Options()
edge_options.add_argument('--disable-notifications')
edge_options.add_argument('--disable-infobars')
edge_options.add_argument('start-maximized')
edge_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0")
edge_options.add_argument("--profile-directory=Default")
edge_options.add_argument(f"--user-data-dir=/home/ajusd/.config/microsoft-edge-dev/Default")
edge_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

# === Launch Edge WebDriver ===
browser = webdriver.Edge(options=edge_options)

# === Open Lazada Product Page ===
# url = "https://www.lazada.co.id/products/nr-hair-tonic-200ml-i9343376-s11864174.html"
# url = "https://www.tokopedia.com/elysiabrandedstuff/maureen-flat-black-leather-gold-sz-35?source=homepage.top_carousel.0.38456"
# url = "https://www.tokopedia.com/collinsofficial/apple-iphone-13-128gb-256gb-512gb-a15-bionic-cpu-6c-gpu-4c-resmi-ibox-midnight-black-128-gb-be0a3?t_id=1747411890139&t_st=1&t_pp=homepage&t_efo=pure_goods_card&t_ef=homepage&t_sm=rec_homepage_outer_flow&t_spt=homepage"

# === LINK ALAS KAKI ===
# url = "https://www.tokopedia.com/porto-footwear/porto-blt-flatshoes-tali-wanita-balet-casual-sepatu-kerja-sepatu-sekolah-black-burgundy-tortilla-1730248189011396169?extParam=ivf%3Dfalse%26search_id%3D2025051719263005679316FD8E422AA5NF"
# url = "https://www.tokopedia.com/caraka-footwear/sepatu-formal-loafers-pria-hitam-original-caraka-footwear-sepatu-formal-casual-pria-keren-elegan-sepatu-loafers-kerja-pria-flat-1729604391726320043?extParam=ivf%3Dfalse%26keyword%3Dloafers%26search_id%3D20250517203746456EC003EFFE56221MEK%26src%3Dsearch&t_id=1747514291875&t_st=1&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/nuevo-offcl-shop/nuevo-velocity-putih-silver-sepatu-sneakers-running-olahraga-lari-pria-outdoor-1729603895625288459?extParam=ivf%3Dfalse%26keyword%3Dsneakers%26search_id%3D20250518042349448EC13E9B47981C4J66%26src%3Dsearch&t_id=1747543320841&t_st=1&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/rf-footwear/rf-footwear-original-sepatu-sneakers-terbaru-full-putih-sepatu-pria-dan-wanita-full-white-size-37-sampai-44-casual-shoes-kasual-1729634779763411084?extParam=ivf%3Dtrue%26keyword%3Dsneakers%26search_id%3D20250518042349448EC13E9B47981C4J66%26src%3Dsearch&t_id=1747543320841&t_st=2&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/porteegoods/porteegoods-og-derby-pria-kulit-microfiber-sepatu-nongkrong-sepatu-formal-sepatu-nikah-sepatu-kerja-sepatu-pantofel-sepatu-boots-sepatu-wisuda-shoes-hitam-sepatu-starboy-1729990397145418531?extParam=ivf%3Dtrue%26keyword%3Dboots%26search_id%3D20250518051622D29076102C25EA27DUDP%26src%3Dsearch&t_id=1747543320841&t_st=3&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/laviofootwear/sepatu-pria-safety-boots-high-premium-quality-lavio-axel-booster-mood-hiking-proyek-outdoor-touring-1729383488839320902?extParam=ivf%3Dtrue%26keyword%3Dboots%26search_id%3D20250518051622D29076102C25EA27DUDP%26src%3Dsearch&t_id=1747543320841&t_st=4&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/pinkeyofficial/pinkey-p026-sepatu-boots-wanita-flat-korea-premium-quality-cream-36?extParam=ivf%3Dtrue%26keyword%3Dheels%26search_id%3D20250518061052456EC003EFFE5628AACT%26src%3Dsearch&t_id=1747543320841&t_st=5&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/pose-shoes-idn/poseshoes-live-streaming-pose-cloud-bounce-cat-paw-sandal-anti-selip-nyaman-anti-bau-bagian-bawah-lembut-dalam-di-luar-ruangan-pria-dan-wanita-pasangan-rumah-serbaguna-beraneka-warna-kualitas-2024-musim-panas-gaya-panas-shoes-p68101-1730807813095786110?extParam=ivf%3Dtrue%26keyword%3Dsandal+wanita%26search_id%3D202505180632587AA97D0B7160BD00BKSB%26src%3Dsearch%26whid%3D18282543&t_id=1747543320841&t_st=6&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/pose-shoes-idn/livestreaming-ramadan-sale-pose-traveling-sandal-jepit-anti-selip-nyaman-tahan-aus-lampu-dalam-di-luar-ruangan-pria-dan-wanita-santai-serbaguna-kepopuleran-kualitas-2024-musim-panas-gaya-panas-pantai-p3246801-1730635411467568766?extParam=ivf%3Dtrue%26keyword%3Dsandal+wanita%26search_id%3D202505180632587AA97D0B7160BD00BKSB%26src%3Dsearch&t_id=1747543320841&t_st=7&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/sandalkanankiri-438/sakaki-patricia-flat-shoes-sandal-wanita-cantik-dan-elegant-black-1730375624677819605?extParam=ivf%3Dtrue%26keyword%3Dsandal+wanita%26search_id%3D202505180632587AA97D0B7160BD00BKSB%26src%3Dsearch&t_id=1747543320841&t_st=8&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"

# === LINK PAKAIAN PRIA ===
# url = "https://www.tokopedia.com/novoidminds/no-void-minds-aezy-regular-fit-core-t-shirt-charcoal-charcoal-s-59ab9?extParam=ivf%3Dtrue%26keyword%3Dregular+fit+shirt%26search_id%3D202505180737351C292C9EFC5BA40B2DY7%26src%3Dsearch&t_id=1747543320841&t_st=9&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/novoidminds/no-void-minds-litex-heavyweight-cotton-tpf-oversized-core-t-shirt-charcoal-1729752639672845349?t_id=1747543320841&t_st=10&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/novoidminds/no-void-minds-aezy-boxy-fit-core-t-shirt-charcoal-1730998908329755685?t_id=1747543320841&t_st=11&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/cozyclub/cozyclub-frank-polo-knit-shirt-kaos-kerah-pria-kaos-lengan-pendek-baju-brown-panjang-casual-1729625526336981441?extParam=ivf%3Dfalse%26keyword%3Dknit+polo%26search_id%3D20250518083421B98EBC002CD63E004I4Z%26src%3Dsearch&t_id=1747543320841&t_st=13&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=search_result"
# url = "https://www.tokopedia.com/bravo-project/kaos-polo-knit-pria-austin-premium-1729964829401385267?extParam=ivf%3Dfalse%26keyword%3Dknit+polo%26search_id%3D20250518083421B98EBC002CD63E004I4Z%26src%3Dsearch&t_id=1747543320841&t_st=14&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/froyemul/froyemul-light-grey-trouser-celana-bahan-pria-formal-slimfit-38?extParam=ivf%3Dtrue%26keyword%3Dcelana+pria&src=topads&t_id=1747543320841&t_st=15&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/juragankauskaki/celana-panjang-jogger-training-olahraga-lari-gym-joger-pria-garis-3xl?extParam=ivf%3Dfalse%26keyword%3Dcelana+pria&src=topads&t_id=1747543320841&t_st=16&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/delibraofficialshop/delibra-jaket-canvas-bomber-pria-premium-lembut-nyaman-casual-distro-keren-1729427606270019600?extParam=ivf%3Dfalse%26keyword%3Djaket+pria%26search_id%3D20250518103245F6DD0C7EEF473B034W4P%26src%3Dsearch&t_id=1747543320841&t_st=39&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/acsgrosir-291/jaket-jeans-pria-slimfit-dark-abu-lengan-panjang-denim-jaket-formal-cowok-distro-bandung-keren-hitam-casual-1729384497051632964?extParam=ivf%3Dfalse%26keyword%3Djaket+pria%26search_id%3D20250518103245F6DD0C7EEF473B034W4P%26src%3Dsearch&t_id=1747543320841&t_st=40&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/delibraofficialshop/delibra-jaket-bomber-suede-pria-premium-1729427766461892624?extParam=ivf%3Dfalse%26keyword%3Djaket+pria%26search_id%3D20250518103245F6DD0C7EEF473B034W4P%26src%3Dsearch&t_id=1747543320841&t_st=41&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/houseofsmithofficial/house-of-smith-harrington-jacket-hangor-black-6-jaket-harrington-pria-hitam-1729385454017348778?extParam=ivf%3Dfalse%26keyword%3Djaket+pria%26search_id%3D20250518103245F6DD0C7EEF473B034W4P%26src%3Dsearch&t_id=1747543320841&t_st=42&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/jiniso/jiniso-loose-denim-jeans-pria-816-28?extParam=ivf%3Dtrue%26keyword%3Djeans+pria%26search_id%3D20250518103526DBCA3B239FC358053OL4%26src%3Dsearch&t_id=1747543320841&t_st=43&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/gizmoclothes/gizmo-celana-jeans-wide-leg-wisker-lebar-gombrong-skena-black-wisker-pria-loose-straight-fit-jumbo-big-keren-bahan-denim-nyaman-oversize-panjang-santai-hitam-dark-casual-1729736875837261305?extParam=ivf%3Dfalse%26keyword%3Djeans+pria%26search_id%3D20250518103526DBCA3B239FC358053OL4%26src%3Dsearch&t_id=1747543320841&t_st=44&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/lw-pria/celana-jeans-pria-celana-panjang-pria-celana-kulot-pria-boyfriend-gombrang-straight-jeans-baggy-pants-celana-denim-pants-celana-cowo-oversize-loose-pants-cowok-1730007327693179856?extParam=ivf%3Dfalse%26keyword%3Djeans+pria%26search_id%3D20250518103526DBCA3B239FC358053OL4%26src%3Dsearch&t_id=1747543320841&t_st=45&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"


# === LINK PAKAIAN WANITA ===
# url = "https://www.tokopedia.com/istana-fashion11/april-top-atasan-wanita-korean-top-baju-knit-basic-long-sleeve-april-top-panjang-kemeja-bona-viral-1730393737063335819?extParam=ivf%3Dfalse%26keyword%3Dkemeja+knit+long%26search_id%3D20250518095826F6DD0C7EEF473B031PH7%26src%3Dsearch&t_id=1747543320841&t_st=17&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url =  "https://www.tokopedia.com/orloid-883/september-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-pendek-basic-short-sleeve-1729580958718460989?t_id=1747543320841&t_st=18&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_3_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/orloid-883/march-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-panjang-basic-long-sleeve-1729580057223201853?t_id=1747543320841&t_st=19&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/orloid-883/leo-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-pendek-basic-short-sleeve-tee-1729855962093422653?t_id=1747543320841&t_st=20&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/orloid-883/july-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-panjang-basic-long-sleeve-1729580954813367357?t_id=1747543320841&t_st=21&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_1_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/orloid-883/february-top-atasan-knit-wanita-korean-top-baju-knit-wanita-lengan-panjang-basic-long-sleeve-1729580053492827197?t_id=1747543320841&t_st=22&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_3_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/cheron-587/cheron-23314-kaos-crop-wanita-remaja-dewasa-polos-murah-santai-crew-neck-katun-hitam-putih-merah-baju-biru-basic-tee-croptop-ungu-baby-tee-1729859677325920393?extParam=ivf%3Dfalse%26keyword%3Dbaby+tee+wanita%26search_id%3D202505181009411C292C9EFC5BA40B54ZZ%26src%3Dsearch&t_id=1747543320841&t_st=23&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_3_module&t_spt=search_result"
# url = "https://www.tokopedia.com/ever-tops/evertops-long-yuka-top-kaos-wanita-atasan-tee-t-shirt-slim-fitting-1729387656897660298?extParam=ivf%3Dfalse%26keyword%3Dkaos+wanita%26search_id%3D20250518101035448EC13E9B4798094GMD%26src%3Dsearch&t_id=1747543320841&t_st=24&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/diansofficial/dians-rok-span-panjang-scuba-premium-rok-pensil-bahan-kantor-formal-wanita-kerja-maxy-skirt-hitam-muslim-maxi-basic-bawahan-casual-rempel-karet-rok-span-tanpa-belahan-outfit-muslimah-1730221062170576547?extParam=ivf%3Dtrue%26keyword%3Dbawahan+wanita%26search_id%3D20250518101350B98EBC002CD63E092Y8U%26src%3Dsearch&t_id=1747543320841&t_st=25&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/anjana-fashion/rok-cargo-wanita-span-panjang-tebal-skirt-bawahan-american-drill-standar-fit-hitam-kerja-formal-1730170430222926855?extParam=ivf%3Dfalse%26keyword%3Dbawahan+wanita%26search_id%3D20250518101350B98EBC002CD63E092Y8U%26src%3Dsearch&t_id=1747543320841&t_st=26&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/tiarastorre/rok-rajut-span-7-8-se-betis-rok-kerja-formal-kekinian-polos-nyaman-panjang-abu-hitam-tebal-kantor-coklat-wanita-navy-1729436215594224477?t_id=1747543320841&t_st=27&t_pp=product_detail&t_efo=horizontal_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_3_module&t_spt=product_detail"
# url = "https://www.tokopedia.com/hulmofficial/kemeja-loose-fit-wanita-aina-shirt-hulm-katun-lembut-1730639007144183406?extParam=ivf%3Dfalse%26keyword%3Dkemeja+wanita%26search_id%3D20250518102205456EC003EFFE563B0VQ4%26src%3Dsearch&t_id=1747543320841&t_st=28&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=rec_product_detail_outer_pdp_3_module&t_spt=search_result"
# url = "https://www.tokopedia.com/wispie/wispie-money-magnet-fitted-shirt-kemeja-kerja-wanita-press-body-pinstripe-salur-pink-biru-berkaret-1729770611997508995?extParam=ivf%3Dfalse%26keyword%3Dkemeja+wanita%26search_id%3D20250518102205456EC003EFFE563B0VQ4%26src%3Dsearch&t_id=1747543320841&t_st=29&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/wispie/wispie-city-pants-celana-tidur-tipis-panjang-wanita-kantor-kuliah-motif-garis-kulot-pinstripe-karet-lembut-loose-1730336306803934595?extParam=ivf%3Dfalse%26keyword%3Dpants+wanita%26search_id%3D20250518102410E4EF27D983B7A216BHOV%26src%3Dsearch&t_id=1747543320841&t_st=30&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/eijiidstore-451/eiji-flare-pants-highwaist-flare-pants-celana-kulot-semi-cutbray-wanita-1729858688496143257?extParam=ivf%3Dfalse%26keyword%3Dpants+wanita%26search_id%3D20250518102410E4EF27D983B7A216BHOV%26src%3Dsearch&t_id=1747543320841&t_st=31&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/lulu-jeans-store/lulu-jeans-new-korean-style-high-waist-loose-murah-celana-jeans-panjang-wanita-1731405016523769077?extParam=ivf%3Dfalse%26keyword%3Djeans+wanita%26search_id%3D20250518102640E99F3F53DAD4C1196ZX5%26src%3Dsearch&t_id=1747543320841&t_st=32&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/jiniso/weekend-jiniso-oversize-baggy-loose-celana-jeans-wanita-highwaist-1729559822014711764?extParam=ivf%3Dtrue%26keyword%3Djeans+wanita%26search_id%3D20250518102640E99F3F53DAD4C1196ZX5%26src%3Dsearch&t_id=1747543320841&t_st=33&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/binzzaeco/highwaist-cutbray-jeans-wanita-celana-panjang-denim-cutbray-hitam-melar-nyaman-kaki-basic-1729604087170566020?extParam=ivf%3Dfalse%26keyword%3Djeans+wanita%26search_id%3D20250518102640E99F3F53DAD4C1196ZX5%26src%3Dsearch&t_id=1747543320841&t_st=34&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/nz-fashion/celana-highwaist-loose-jeans-wanita-baggy-jeans-loose-highwaist-1730598928112715175?extParam=ivf%3Dfalse%26keyword%3Djeans+wanita%26search_id%3D20250518102640E99F3F53DAD4C1196ZX5%26src%3Dsearch&t_id=1747543320841&t_st=35&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/hanafashionjkt/hana-fashion-arisha-casual-long-dress-dress-maxi-wanita-cd047-2-dress-panjang-baju-lebaran-1729613246210804339?extParam=ivf%3Dtrue%26keyword%3Ddress+wanita%26search_id%3D20250518103032B98EBC002CD63E2C1K8P%26src%3Dsearch&t_id=1747543320841&t_st=37&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"
# url = "https://www.tokopedia.com/firda-fashion-862/dress-kaftan-batik-elegan-wanita-pesta-aruna-1729615492746545673?extParam=ivf%3Dfalse%26keyword%3Ddress+wanita%26search_id%3D20250518103032B98EBC002CD63E2C1K8P%26src%3Dsearch&t_id=1747543320841&t_st=38&t_pp=search_result&t_efo=search_pure_goods_card&t_ef=goods_search&t_sm=&t_spt=search_result"


browser.get(url)

close_popup_if_exists(browser)

# === Wait and Scrape Product Info ===
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
    if product_name:
        print(f"🔹 Product Name Detected: {product_name}")
    else:
        product_name_tag = soup.find("h1", class_="css-14yroid")
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else None

        if product_name:
            print(f"🔹 Product Name Detected: {product_name}")
        else:
            print("❌ Product name not found.")

    # === NEW: Get Product Prices ===
    current_price_tag = soup.find("div", {"data-testid": "lblPDPDetailProductPrice"})
    original_price_tag = soup.find("span", {"data-testid": "lblPDPDetailOriginalPrice"})

    current_price = current_price_tag.get_text(strip=True) if current_price_tag else "-"
    original_price = original_price_tag.get_text(strip=True) if original_price_tag else "-"

    print(f"💰 Current Price : {current_price}")
    print(f"💸 Original Price: {original_price}")

    # === NEW: Get Product Image URL ===
    image_tag = soup.find("img", {"data-testid": "PDPMainImage"})
    image_url = image_tag["src"] if image_tag and image_tag.has_attr("src") else "-"
    print(f"🖼️ Image URL     : {image_url}")

    # === NEW: Get Stock Quantity ===
    stock_tag = soup.find("p", {"data-testid": "stock-label"})
    stock_value = "-"
    if stock_tag:
        bold_tag = stock_tag.find("b")
        if bold_tag:
            stock_value = bold_tag.get_text(strip=True)

    print(f"📦 Stock        : {stock_value}")

    # Prepare data as a dict (single row), but without item_id yet
    product_data = {
        "Product Name": product_name or "-",
        "Current Price": current_price,
        "Original Price": original_price,
        "Image URL": image_url,
        "Stock": stock_value
    }

    # Create filename (assuming `category` is a string with the filename)
    filename = category

    if os.path.exists(filename):
        # Read existing CSV to count rows
        existing_df = pd.read_csv(filename)
        existing_rows = len(existing_df)

        # New item_id is next number
        item_id = existing_rows + 1
        product_data['item_id'] = item_id

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Append without header
        df.to_csv(filename, mode='a', index=False, header=False)
        print(f"💾 Appended product info as item_id {item_id} to existing file: {filename}")

    else:
        # First entry, item_id = 1
        product_data['item_id'] = 1

        # Convert to DataFrame
        df = pd.DataFrame([product_data])

        # Write new file with header
        df.to_csv(filename, index=False)
        print(f"💾 Created new file and saved product info as item_id 1: {filename}")
    
    # === ✅ Scroll to Review Section Immediately After Stock Check ===
    try:
        print("🧭 Scrolling to review section...")
        # sleep for visibility of change
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

    all_reviews = []
    page_number = 1

    while True:
        print(f"\n📖 Scraping review page {page_number}...\n")

        # === Scroll to Reviews Section ===
        try:
            review_container = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "review-feed"))
            )
            browser.execute_script("arguments[0].scrollIntoView();", review_container)
            sleep(2)
        except:
            print("⚠️ Review section not found or not visible yet.")

        # Refresh soup after scroll
        # html = browser.execute_script("return document.documentElement.innerHTML")
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        # === Find All Reviews ===
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

        # === Try to Click Next Button ===
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

    # After while loop (when all reviews collected)
    if all_reviews:
        print(f"✅ Total reviews collected: {len(all_reviews)}")
        df = pd.DataFrame(all_reviews)
        filename = f"{product_name[:50].replace(' ', '_').replace('/', '_')}_reviews.csv"
        df.to_csv(filename, index=False)
        print(f"💾 Reviews saved to: {filename}")
    else:
        print("⚠️ No reviews collected.")

except Exception as e:
    print(f"❌ Error during scraping: {e}")
    #     print("❌ Product detail not found.")

except TimeoutException:
    print("❌ Page load timeout!")

finally:
    browser.quit()
