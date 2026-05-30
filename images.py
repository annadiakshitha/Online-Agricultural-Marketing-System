# ============================================================
#  AgriMarket — Complete Image Reference File
#  images.py
#
#  HOW TO USE:
#  1. This file lists ALL images used across the entire project
#  2. To add a new product image:
#     a) Go to https://unsplash.com
#     b) Search for your product (e.g. "cauliflower farm fresh")
#     c) Click the photo → right-click → "Copy image address"
#     d) Add it to the PRODUCT_IMAGES dict below
#     e) Use that URL when adding a new product in the website
#  3. To replace a background/hero image, update BACKGROUND_IMAGES
#  4. All URLs use ?w=700&q=85 for good quality + fast loading
# ============================================================


# ============================================================
#  SECTION 1: HERO / BACKGROUND IMAGES  (used in HTML templates)
# ============================================================
BACKGROUND_IMAGES = {

    # Homepage hero — full-screen background (index.html)
    "homepage_hero": "https://images.unsplash.com/photo-1500651230702-0e2d8a49d4ad?w=1920&q=90",
    # Description: Aerial view of lush green farm fields at sunrise

    # Dark CTA banner on homepage (index.html)
    "homepage_cta_banner": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=1600&q=85",
    # Description: Farmer's hands holding freshly harvested vegetables

    # Farmer spotlight / mission section (index.html)
    "farmer_spotlight": "https://images.unsplash.com/photo-1589923158776-cb4485d99fd6?w=900&q=85",
    # Description: Indian farmer standing in lush green crop field

    # Login page side visual (login.html)
    "login_side_photo": "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=900&q=85",
    # Description: Fresh vegetables and herbs at a market

    # Register page side visual (register.html)
    "register_side_photo": "https://images.unsplash.com/photo-1595273670150-bd0c3c392e46?w=900&q=85",
    # Description: Wheat field at golden hour sunset

    # Shop page hero banner (products.html)
    "shop_hero": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=1600&q=85",
    # Description: Colorful fresh produce at an Indian market

    # Fallback image — shown if any product image fails to load
    "fallback_product": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?w=600&q=80",
    # Description: Generic assorted fresh vegetables

}


# ============================================================
#  SECTION 2: PRODUCT IMAGES  (used in database + product cards)
# ============================================================
#  Format: "product_key": ("URL", "Product Name", "Category")
# ============================================================

PRODUCT_IMAGES = {

    # ── VEGETABLES ──────────────────────────────────────────
    "tomatoes_farm_fresh": (
        "https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=700&q=85",
        "Farm Fresh Tomatoes", "Vegetables"
    ),
    "tomatoes_cherry": (
        "https://images.unsplash.com/photo-1546470427-0d4e0b9a06a4?w=700&q=85",
        "Cherry Tomatoes", "Vegetables"
    ),
    "capsicum_green": (
        "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=700&q=85",
        "Green Capsicum", "Vegetables"
    ),
    "onions_nashik": (
        "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=700&q=85",
        "Nashik Onions", "Vegetables"
    ),
    "garlic_white": (
        "https://images.unsplash.com/photo-1615477550927-6ec8445b07a8?w=700&q=85",
        "White Garlic Bulbs", "Vegetables"
    ),
    "potatoes_baby": (
        "https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=700&q=85",
        "Baby Potatoes", "Vegetables"
    ),
    "cluster_beans": (
        "https://images.unsplash.com/photo-1566486189376-d5f21e25aae4?w=700&q=85",
        "Rajasthani Cluster Beans", "Vegetables"
    ),
    "brinjal_purple": (
        "https://images.unsplash.com/photo-1615484477778-ca3b77940c25?w=700&q=85",
        "Purple Brinjal", "Vegetables"
    ),
    "okra_bhendi": (
        "https://images.unsplash.com/photo-1632245889029-e406faaa34cd?w=700&q=85",
        "Bhendi (Ladies Finger)", "Vegetables"
    ),
    "carrots_organic": (
        "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=700&q=85",
        "Organic Carrots", "Vegetables"
    ),
    "cucumber_mysore": (
        "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=700&q=85",
        "Mysore Cucumber", "Vegetables"
    ),
    "bitter_gourd_karela": (
        "https://images.unsplash.com/photo-1626200919957-01c6b8148e41?w=700&q=85",
        "Bitter Gourd (Karela)", "Vegetables"
    ),
    "sweet_corn": (
        "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=700&q=85",
        "Sweet Corn Cobs", "Vegetables"
    ),
    "green_peas": (
        "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=700&q=85",
        "Green Peas (Matar)", "Vegetables"
    ),

    # ── ADDITIONAL VEGETABLES (ready to add) ─────────────────
    "cauliflower": (
        "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=700&q=85",
        "Fresh Cauliflower", "Vegetables"
    ),
    "cabbage": (
        "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=700&q=85",
        "Green Cabbage", "Vegetables"
    ),
    "beetroot": (
        "https://images.unsplash.com/photo-1593105544559-ecb03bf76f82?w=700&q=85",
        "Fresh Beetroot", "Vegetables"
    ),
    "pumpkin": (
        "https://images.unsplash.com/photo-1570586437263-ab629fccc818?w=700&q=85",
        "Orange Pumpkin", "Vegetables"
    ),
    "radish": (
        "https://images.unsplash.com/photo-1587411768638-ec71f8e33b78?w=700&q=85",
        "White Radish (Mooli)", "Vegetables"
    ),
    "sweet_potato": (
        "https://images.unsplash.com/photo-1596097635121-14b38c5d7a55?w=700&q=85",
        "Sweet Potato (Shakarkandi)", "Vegetables"
    ),

    # ── LEAFY GREENS ─────────────────────────────────────────
    "spinach_baby": (
        "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=700&q=85",
        "Baby Spinach Leaves", "Leafy Greens"
    ),
    "methi_fenugreek": (
        "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=700&q=85",
        "Methi (Fenugreek Leaves)", "Leafy Greens"
    ),
    "curry_leaves": (
        "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85",
        "Kerala Curry Leaves", "Leafy Greens"
    ),
    "moringa_drumstick": (
        "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=700&q=85",
        "Drumstick Leaves (Moringa)", "Leafy Greens"
    ),
    "amaranth_rajgira": (
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&q=85",
        "Amaranth (Rajgira) Leaves", "Leafy Greens"
    ),

    # ── ADDITIONAL LEAFY GREENS (ready to add) ───────────────
    "coriander_fresh": (
        "https://images.unsplash.com/photo-1599201316840-7e6b6b421e14?w=700&q=85",
        "Fresh Coriander (Dhaniya)", "Leafy Greens"
    ),
    "mint_pudina": (
        "https://images.unsplash.com/photo-1628557044797-f21a177c37ec?w=700&q=85",
        "Fresh Mint (Pudina)", "Leafy Greens"
    ),
    "palak_amaranth": (
        "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=700&q=85",
        "Palak (Spinach Bunch)", "Leafy Greens"
    ),

    # ── FRUITS ───────────────────────────────────────────────
    "mango_alphonso": (
        "https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=700&q=85",
        "Alphonso Mangoes", "Fruits"
    ),
    "strawberry_ooty": (
        "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=700&q=85",
        "Ooty Strawberries", "Fruits"
    ),
    "banana_nendran": (
        "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=700&q=85",
        "Nendran Bananas", "Fruits"
    ),
    "orange_coorg": (
        "https://images.unsplash.com/photo-1548103614-609e3e1c7d03?w=700&q=85",
        "Coorg Oranges", "Fruits"
    ),
    "kiwi_darjeeling": (
        "https://images.unsplash.com/photo-1618897996318-5a901fa6ca71?w=700&q=85",
        "Darjeeling Kiwi", "Fruits"
    ),
    "pomegranate_jaisalmer": (
        "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=700&q=85",
        "Jaisalmer Pomegranate", "Fruits"
    ),
    "litchi_muzaffarpur": (
        "https://images.unsplash.com/photo-1598511726623-d2e9996892f5?w=700&q=85",
        "Litchi from Muzaffarpur", "Fruits"
    ),

    # ── ADDITIONAL FRUITS (ready to add) ─────────────────────
    "papaya": (
        "https://images.unsplash.com/photo-1526318896980-cf78c088247c?w=700&q=85",
        "Fresh Papaya", "Fruits"
    ),
    "guava": (
        "https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=700&q=85",
        "Fresh Guava (Amrood)", "Fruits"
    ),
    "watermelon": (
        "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=700&q=85",
        "Seedless Watermelon", "Fruits"
    ),
    "grapes_black": (
        "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=700&q=85",
        "Black Grapes (Nasik)", "Fruits"
    ),
    "sapota_chikoo": (
        "https://images.unsplash.com/photo-1617312401574-d7afa1df18f2?w=700&q=85",
        "Sapota (Chikoo)", "Fruits"
    ),
    "coconut_fresh": (
        "https://images.unsplash.com/photo-1559181567-c3190ca9be46?w=700&q=85",
        "Fresh Green Coconut", "Fruits"
    ),

    # ── GRAINS ───────────────────────────────────────────────
    "basmati_rice_premium": (
        "https://images.unsplash.com/photo-1536304993881-ff86e0c9b31c?w=700&q=85",
        "Premium Basmati Rice", "Grains"
    ),
    "moong_dal_yellow": (
        "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=700&q=85",
        "Yellow Moong Dal", "Grains"
    ),
    "sona_masoori_rice": (
        "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=700&q=85",
        "Sona Masoori Rice", "Grains"
    ),
    "urad_dal_black": (
        "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=700&q=85",
        "Black Urad Dal (Whole)", "Grains"
    ),
    "jowar_sorghum": (
        "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85",
        "Jowar (Sorghum)", "Grains"
    ),
    "bajra_millet": (
        "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85",
        "Bajra (Pearl Millet)", "Grains"
    ),
    "mustard_seeds": (
        "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=700&q=85",
        "Bengal Mustard Seeds", "Grains"
    ),

    # ── ADDITIONAL GRAINS (ready to add) ─────────────────────
    "wheat_atta": (
        "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85",
        "Whole Wheat (Gehun)", "Grains"
    ),
    "chana_dal": (
        "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=700&q=85",
        "Chana Dal (Split Bengal Gram)", "Grains"
    ),
    "toor_dal": (
        "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=700&q=85",
        "Toor Dal (Arhar)", "Grains"
    ),
    "ragi_finger_millet": (
        "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85",
        "Ragi (Finger Millet)", "Grains"
    ),
    "quinoa_organic": (
        "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=700&q=85",
        "Organic Quinoa", "Grains"
    ),

    # ── DAIRY & HONEY ────────────────────────────────────────
    "milk_a2_gir": (
        "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85",
        "A2 Gir Cow Milk", "Dairy & Honey"
    ),
    "honey_raw_forest": (
        "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=700&q=85",
        "Raw Forest Honey", "Dairy & Honey"
    ),
    "ghee_desi_bilona": (
        "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=700&q=85",
        "Pure Desi Ghee (Bilona)", "Dairy & Honey"
    ),
    "honey_wildflower_coorg": (
        "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=700&q=85",
        "Coorg Wildflower Honey", "Dairy & Honey"
    ),
    "coconut_oil_kerala": (
        "https://images.unsplash.com/photo-1617132999740-45e4fcda3a62?w=700&q=85",
        "Kerala Coconut Oil", "Dairy & Honey"
    ),
    "mishti_doi_bengal": (
        "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85",
        "Mishti Doi (Sweet Curd)", "Dairy & Honey"
    ),

    # ── ADDITIONAL DAIRY (ready to add) ──────────────────────
    "curd_dahi_fresh": (
        "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85",
        "Fresh Dahi (Curd)", "Dairy & Honey"
    ),
    "paneer_fresh": (
        "https://images.unsplash.com/photo-1628557044797-f21a177c37ec?w=700&q=85",
        "Fresh Paneer", "Dairy & Honey"
    ),
    "buttermilk_chaas": (
        "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85",
        "Buttermilk (Chaas)", "Dairy & Honey"
    ),
    "beeswax_pure": (
        "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=700&q=85",
        "Pure Beeswax", "Dairy & Honey"
    ),

    # ── SPICES ───────────────────────────────────────────────
    "chilli_kashmiri_red": (
        "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=700&q=85",
        "Kashmiri Red Chilli Powder", "Spices"
    ),
    "pepper_chettinad": (
        "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85",
        "Chettinad Pepper Powder", "Spices"
    ),
    "cardamom_kerala": (
        "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85",
        "Kerala Cardamom", "Spices"
    ),
    "turmeric_coorg": (
        "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=700&q=85",
        "Coorg Turmeric Fingers", "Spices"
    ),
    "star_anise": (
        "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85",
        "Star Anise (Chakra Phool)", "Spices"
    ),
    "coriander_seeds": (
        "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85",
        "Punjabi Coriander Seeds", "Spices"
    ),

    # ── ADDITIONAL SPICES (ready to add) ─────────────────────
    "cumin_jeera": (
        "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85",
        "Cumin Seeds (Jeera)", "Spices"
    ),
    "cinnamon_dalchini": (
        "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85",
        "Cinnamon (Dalchini)", "Spices"
    ),
    "cloves_laung": (
        "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85",
        "Cloves (Laung)", "Spices"
    ),
    "fenugreek_seeds": (
        "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=700&q=85",
        "Fenugreek Seeds (Methi Dana)", "Spices"
    ),
    "saffron_kesar": (
        "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85",
        "Kashmiri Saffron (Kesar)", "Spices"
    ),
    "dry_ginger_saunth": (
        "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=700&q=85",
        "Dry Ginger (Saunth)", "Spices"
    ),
}


# ============================================================
#  SECTION 3: HOW TO ADD A NEW IMAGE TO THE PROJECT
# ============================================================
#
#  STEP 1 — Find your image on Unsplash:
#    → Go to https://unsplash.com
#    → Search for your product e.g. "fresh cauliflower india"
#    → Click the best photo
#    → Copy the photo URL from your browser address bar
#      (e.g. https://images.unsplash.com/photo-XXXXXX)
#    → Append: ?w=700&q=85  for fast loading
#
#  STEP 2 — Add it to PRODUCT_IMAGES above:
#    "my_product_key": (
#        "https://images.unsplash.com/photo-XXXXXX?w=700&q=85",
#        "My Product Name",
#        "Category"
#    ),
#
#  STEP 3 — Use it when listing a product on the website:
#    → Login as a Farmer
#    → Go to Dashboard → Add Product
#    → Paste the URL in the "Product Photo URL" field
#
#  STEP 4 (Optional) — Use it directly in app.py dataset:
#    → Open app.py → find the products_data list
#    → Add a new tuple with your image URL
#
# ============================================================
#  SECTION 4: IMAGE SIZING GUIDE
# ============================================================
#
#  Use these URL parameters for different contexts:
#
#  Product cards (small):     ?w=400&q=80
#  Product detail (large):    ?w=700&q=85
#  Hero banners (full-width): ?w=1920&q=90
#  Thumbnails (tiny):         ?w=200&q=70
#
#  Example:
#  https://images.unsplash.com/photo-1607305387299?w=700&q=85
#                                                   ↑ width   ↑ quality (0-100)
#
# ============================================================
#  SECTION 5: HELPER FUNCTION — Get image URL by key
# ============================================================

def get_image_url(key, size="medium"):
    """
    Get an image URL by its key name.
    size options: 'small' (400px), 'medium' (700px), 'large' (1200px), 'hero' (1920px)
    """
    sizes = {
        "small":  "?w=400&q=80",
        "medium": "?w=700&q=85",
        "large":  "?w=1200&q=85",
        "hero":   "?w=1920&q=90",
    }
    suffix = sizes.get(size, "?w=700&q=85")

    if key in PRODUCT_IMAGES:
        base_url = PRODUCT_IMAGES[key][0].split("?")[0]
        return base_url + suffix

    if key in BACKGROUND_IMAGES:
        base_url = BACKGROUND_IMAGES[key].split("?")[0]
        return base_url + suffix

    return BACKGROUND_IMAGES["fallback_product"]


def list_all_images():
    """Print a summary of all images in the project."""
    print("=" * 60)
    print("  AGRIMARKET — ALL IMAGES SUMMARY")
    print("=" * 60)
    print(f"\n📸 BACKGROUND / HERO IMAGES ({len(BACKGROUND_IMAGES)} total)")
    for key, url in BACKGROUND_IMAGES.items():
        print(f"  [{key}]\n   → {url}\n")

    from collections import defaultdict
    by_cat = defaultdict(list)
    for key, (url, name, cat) in PRODUCT_IMAGES.items():
        by_cat[cat].append((key, name, url))

    print(f"\n🌿 PRODUCT IMAGES ({len(PRODUCT_IMAGES)} total)")
    for cat in sorted(by_cat.keys()):
        print(f"\n  ── {cat.upper()} ({len(by_cat[cat])} images) ──")
        for key, name, url in sorted(by_cat[cat]):
            print(f"  [{key}] {name}")
            print(f"   → {url}")


if __name__ == "__main__":
    list_all_images()
    print("\n" + "=" * 60)
    print("  EXAMPLE USAGE:")
    print("=" * 60)
    url = get_image_url("tomatoes_farm_fresh", "medium")
    print(f"\n  get_image_url('tomatoes_farm_fresh', 'medium')")
    print(f"  → {url}")
    url2 = get_image_url("homepage_hero", "hero")
    print(f"\n  get_image_url('homepage_hero', 'hero')")
    print(f"  → {url2}")
