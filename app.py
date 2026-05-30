from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3, hashlib, random, string
from functools import wraps
from translations import TRANSLATIONS, LANGUAGES, t, get_all_for_lang

app = Flask(__name__)
app.secret_key = 'agrimarket_2024_ultra_secure'
DB = 'agrimarket.db'

# ── LANGUAGE HELPERS ─────────────────────────────────────────────────────────
def get_lang():
    return session.get('lang', 'en')

def inject_lang():
    """Returns translation dict + language meta for current session language."""
    lang = get_lang()
    return {
        'T': get_all_for_lang(lang),
        'lang': lang,
        'LANGUAGES': LANGUAGES,
        'lang_name': LANGUAGES[lang]['native'],
        'lang_flag': LANGUAGES[lang]['flag'],
    }

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def hp(p): return hashlib.sha256(p.encode()).hexdigest()
def txn_id(): return 'AGM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def login_req(f):
    @wraps(f)
    def w(*a, **k):
        if 'uid' not in session: return redirect(url_for('login'))
        return f(*a, **k)
    return w

def farmer_req(f):
    @wraps(f)
    def w(*a, **k):
        if session.get('role') != 'farmer': return redirect(url_for('dashboard'))
        return f(*a, **k)
    return w

def init_db():
    conn = db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            phone TEXT DEFAULT '',
            location TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            unit TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            description TEXT DEFAULT '',
            image_url TEXT DEFAULT '',
            badge TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(farmer_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            farmer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            payment_method TEXT DEFAULT 'card',
            payment_id TEXT DEFAULT '',
            delivery_address TEXT DEFAULT '',
            delivery_name TEXT DEFAULT '',
            delivery_phone TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    # ── 15 FARMERS ───────────────────────────────────────────────────────────
    farmers_raw = [
        ("Akshitha",          "chikki@farm.com",       "farmer", "9876543210", "Warangal, Telangana"),
        ("Suresh Patel",        "suresh@farm.com",     "farmer", "9845012345", "Nashik, Maharashtra"),
        ("Annamalai Raj",       "anna@farm.com",       "farmer", "9731245678", "Coimbatore, Tamil Nadu"),
        ("Gurpreet Singh",      "gurpreet@farm.com",   "farmer", "9988776655", "Amritsar, Punjab"),
        ("Meena Devi",          "meena@farm.com",      "farmer", "9654321098", "Jaipur, Rajasthan"),
        ("Krishnamurthy V",     "krish@farm.com",      "farmer", "9543210987", "Mysuru, Karnataka"),
        ("Rajesh Yadav",        "rajesh@farm.com",     "farmer", "9432109876", "Patna, Bihar"),
        ("Fatima Shaikh",       "fatima@farm.com",     "farmer", "9321098765", "Aurangabad, Maharashtra"),
        ("Bimal Chandra",       "bimal@farm.com",      "farmer", "9210987654", "Kolkata, West Bengal"),
        ("Lakshmi Nair",        "lakshmi@farm.com",    "farmer", "9109876543", "Thrissur, Kerala"),
        ("Dharampal Bishnoi",   "dharampal@farm.com",  "farmer", "9098765432", "Bikaner, Rajasthan"),
        ("Savitri Reddy",       "savitri@farm.com",    "farmer", "9087654321", "Guntur, Andhra Pradesh"),
        ("Harpreet Kaur",       "harpreet@farm.com",   "farmer", "9076543210", "Ludhiana, Punjab"),
        ("Mohammed Irfan",      "irfan@farm.com",      "farmer", "9065432109", "Hubli, Karnataka"),
        ("Gomathi Sundaram",    "gomathi@farm.com",    "farmer", "9054321098", "Madurai, Tamil Nadu"),
    ]
    fids = []
    for fr in farmers_raw:
        conn.execute("INSERT INTO users(name,email,password,role,phone,location) VALUES(?,?,?,?,?,?)",
                     (fr[0], fr[1], hp("farmer123"), fr[2], fr[3], fr[4]))
        fids.append(conn.execute("SELECT last_insert_rowid()").fetchone()[0])

    # ── 8 CUSTOMERS ──────────────────────────────────────────────────────────
    customers_raw = [
        ("Akshitha",      "chikki@mail.com",    "customer", "9123456789", "Hyderabad, Telangana"),
        ("Arjun Mehta",       "arjun@mail.com",    "customer", "9234567890", "Bengaluru, Karnataka"),
        ("Sneha Kulkarni",    "sneha@mail.com",    "customer", "9345678901", "Pune, Maharashtra"),
        ("Vivek Nambiar",     "vivek@mail.com",    "customer", "9456789012", "Chennai, Tamil Nadu"),
        ("Divya Agarwal",     "divya@mail.com",    "customer", "9567890123", "New Delhi, NCR"),
        ("Rahul Bose",        "rahul@mail.com",    "customer", "9678901234", "Kolkata, West Bengal"),
        ("Ananya Pillai",     "ananya@mail.com",   "customer", "9789012345", "Kochi, Kerala"),
        ("Sameer Joshi",      "sameer@mail.com",   "customer", "9890123456", "Nagpur, Maharashtra"),
    ]
    cids = []
    for cu in customers_raw:
        conn.execute("INSERT INTO users(name,email,password,role,phone,location) VALUES(?,?,?,?,?,?)",
                     (cu[0], cu[1], hp("customer123"), cu[2], cu[3], cu[4]))
        cids.append(conn.execute("SELECT last_insert_rowid()").fetchone()[0])

    f = fids  # shorthand alias

    # ── 60 PRODUCTS ──────────────────────────────────────────────────────────
    # (farmer_id, name, category, price, unit, stock, description, image_url, badge)
    products_data = [

        # ═══ VEGETABLES (18 products) ═══════════════════════════════════════
        (f[0],  "Farm Fresh Tomatoes",       "Vegetables",  45.0,  "kg",    200,
         "Sun-ripened, pesticide-free tomatoes from Telangana's volcanic red soil. Harvested same morning. Rich in lycopene — perfect for curries, chutneys and fresh salads.",
         "https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=700&q=85", "Organic"),

        (f[0],  "Cherry Tomatoes",           "Vegetables",  80.0,  "250g",  140,
         "Sweet bite-sized cherry tomatoes from Telangana greenhouses. Zero pesticides, high natural sugar content. Best straight from the punnet or in caprese salads.",
         "https://images.unsplash.com/photo-1546470427-0d4e0b9a06a4?w=700&q=85", "Organic"),

        (f[0],  "Green Capsicum",            "Vegetables",  60.0,  "kg",    120,
         "Crisp, thick-walled green capsicums grown without chemicals. Excellent for stir-fries, kadai preparations and stuffed capsicum recipes.",
         "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=700&q=85", "Farm Fresh"),

        (f[1],  "Nashik Red Onions",         "Vegetables",  30.0,  "kg",    600,
         "India's most famous onions from Nashik. Pungent, high in quercetin and sulphur compounds. The backbone of every Indian kitchen — raw, cooked or pickled.",
         "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=700&q=85", ""),

        (f[1],  "White Garlic Bulbs",        "Vegetables",  180.0, "250g",  300,
         "Aromatic, firm white garlic from Nashik farms. Intense flavour, no chemical treatment. Sun-dried naturally on the farm after harvest.",
         "https://images.unsplash.com/photo-1615477550927-6ec8445b07a8?w=700&q=85", ""),

        (f[4],  "Baby Potatoes",             "Vegetables",  40.0,  "kg",    400,
         "Tender creamy baby potatoes from Rajasthan's sandy loam soil. Thin skin, buttery texture. Perfect for dum aloo, roasted potatoes and chaat.",
         "https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=700&q=85", ""),

        (f[4],  "Rajasthani Cluster Beans",  "Vegetables",  35.0,  "250g",  180,
         "Tender gawar phali (cluster beans) harvested young for maximum tenderness. High in soluble fibre and protein. Pairs beautifully with besan and spices.",
         "https://images.unsplash.com/photo-1566486189376-d5f21e25aae4?w=700&q=85", "Farm Fresh"),

        (f[6],  "Purple Brinjal",            "Vegetables",  28.0,  "kg",    220,
         "Glossy, meaty purple brinjals from Bihar's alluvial farms. Ideal for bharwa baingan, baingan bharta and South Indian curries. Medium spice.",
         "https://images.unsplash.com/photo-1615484477778-ca3b77940c25?w=700&q=85", ""),

        (f[7],  "Bhendi (Ladies Finger)",    "Vegetables",  42.0,  "500g",  160,
         "Tender, slim okra harvested before they toughen, from Aurangabad's organic farms. Zero pesticides, triple-washed. Best for bhindi masala and sambar.",
         "https://images.unsplash.com/photo-1632245889029-e406faaa34cd?w=700&q=85", "Organic"),

        (f[2],  "Organic Carrots",           "Vegetables",  55.0,  "kg",    180,
         "Sweet, crunchy orange carrots from Tamil Nadu's highland organic farms. No chemical fertilizers. Exceptionally high beta-carotene, great raw or cooked.",
         "https://images.unsplash.com/photo-1447175008436-054170c2e979?w=700&q=85", "Organic"),

        (f[5],  "Mysore Cucumber",           "Vegetables",  30.0,  "kg",    190,
         "Crisp, cool cucumbers from Karnataka's irrigated farms. Dark green, thick-walled, low seeds. Perfect for raita, fresh juice and summer salads.",
         "https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?w=700&q=85", ""),

        (f[7],  "Bitter Gourd (Karela)",     "Vegetables",  38.0,  "500g",  160,
         "Fresh tender karela harvested young — less bitter than mature pods. Known to naturally regulate blood sugar. A staple of traditional Indian medicine.",
         "https://images.unsplash.com/photo-1626200919957-01c6b8148e41?w=700&q=85", ""),

        (f[6],  "Sweet Corn Cobs",           "Vegetables",  25.0,  "piece", 300,
         "Freshly picked sweet corn from Bihar's black alluvial fields. Yellow bicolor variety with high natural sugar. Best eaten within hours of harvest.",
         "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=700&q=85", "Fresh Today"),

        (f[8],  "Fresh Green Peas (Matar)",  "Vegetables",  55.0,  "kg",    200,
         "Fresh-shelled winter green peas from West Bengal. Sweet, starchy, vibrant green. Perfect for matar paneer, pulao and aloo matar curry.",
         "https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=700&q=85", "Seasonal"),

        (f[11], "Guntur Green Chillies",     "Vegetables",  45.0,  "250g",  280,
         "Fiery fresh green chillies from Guntur — India's spice capital. Medium-hot variety, thin skin. Essential for authentic Andhra cuisine.",
         "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=700&q=85", "Hot Pick"),

        (f[11], "Cauliflower (Gobhi)",       "Vegetables",  40.0,  "piece", 200,
         "Large tight-headed white cauliflower from Andhra Pradesh's rich black cotton soil. Crisp, sweet florets. Perfect for aloo gobhi, gobhi manchurian.",
         "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=700&q=85", ""),

        (f[14], "Fresh Beetroot",            "Vegetables",  50.0,  "kg",    150,
         "Deep-crimson beetroot from Tamil Nadu's Ooty hills. High in nitrates, folate and antioxidants. Earthy-sweet flavour, excellent roasted or juiced.",
         "https://images.unsplash.com/photo-1593105544559-ecb03bf76f82?w=700&q=85", ""),

        (f[4],  "Radish (Mooli)",            "Vegetables",  22.0,  "bunch", 220,
         "Crisp white daikon radish from Rajasthan's winter season. Mild, slightly peppery. Essential for mooli paratha, pickles and fresh chutneys.",
         "https://images.unsplash.com/photo-1587411768638-ec71f8e33b78?w=700&q=85", "Winter Fresh"),

        # ═══ LEAFY GREENS (8 products) ══════════════════════════════════════
        (f[0],  "Baby Spinach Leaves",       "Leafy Greens", 60.0, "bunch", 150,
         "Tender young spinach leaves hand-picked at dawn for peak nutrition. Triple-washed, pesticide-free. Rich in iron, folate and vitamins A, C and K.",
         "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=700&q=85", "Farm Fresh"),

        (f[5],  "Methi (Fenugreek Leaves)",  "Leafy Greens", 25.0, "bunch", 200,
         "Fresh slightly-bitter methi from Karnataka's organic farms. Rich in diosgenin and alkaloids. Perfect for methi paratha, dal methi and aloo methi.",
         "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=700&q=85", ""),

        (f[9],  "Kerala Curry Leaves",       "Leafy Greens", 20.0, "bunch", 250,
         "Fragrant fresh curry leaves from Kerala's spice garden farms. Harvested daily at sunrise. The irreplaceable aroma of South Indian tempering.",
         "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85", ""),

        (f[9],  "Moringa (Drumstick) Leaves","Leafy Greens", 30.0, "bunch", 120,
         "Moringa leaves from Kerala — the 'miracle tree'. Exceptional protein, iron, calcium and antioxidant content. Used in dal, sambhar and stir-fries.",
         "https://images.unsplash.com/photo-1471193945509-9ad0617afabf?w=700&q=85", "Superfood"),

        (f[5],  "Amaranth (Rajgira) Leaves", "Leafy Greens", 22.0, "bunch", 140,
         "Tender red and green amaranth leaves from Karnataka. Used in traditional South Indian cuisine. Very high calcium and iron, gluten-free.",
         "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700&q=85", ""),

        (f[14], "Fresh Coriander (Dhaniya)", "Leafy Greens", 15.0, "bunch", 300,
         "Fragrant fresh coriander bunches from Tamil Nadu farms. Packed with volatile oils. Harvested just before shipping. No cold-chain wilting.",
         "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=700&q=85", "Fresh Today"),

        (f[14], "Fresh Mint (Pudina)",       "Leafy Greens", 18.0, "bunch", 200,
         "Freshly cut spearmint bunches. Intensely aromatic. Essential for chutneys, biryanis, raitas and refreshing drinks. No preservatives.",
         "https://images.unsplash.com/photo-1628557044797-f21a177c37ec?w=700&q=85", ""),

        (f[12], "Sarson (Mustard Greens)",   "Leafy Greens", 28.0, "bunch", 160,
         "Fresh sarson leaves from Punjab's winter fields. The star of sarson da saag with makki di roti. Rich in vitamins A, C and K.",
         "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=700&q=85", "Winter Special"),

        # ═══ FRUITS (12 products) ════════════════════════════════════════════
        (f[1],  "Alphonso Mangoes",          "Fruits",      380.0, "dozen", 60,
         "GI-tagged Ratnagiri Alphonsos — the undisputed King of Mangoes. Zero fibre, saffron-gold flesh, intensely aromatic. Seasonal, limited stock. Ships in foam-protected boxes.",
         "https://images.unsplash.com/photo-1591073113125-e46713c829ed?w=700&q=85", "Seasonal"),

        (f[2],  "Ooty Strawberries",         "Fruits",      120.0, "250g",  80,
         "Plump ruby-red strawberries from the Nilgiri hills at 7,000 ft altitude. Naturally sweet, harvested at sunrise. No artificial ripening or wax coating.",
         "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=700&q=85", "Limited"),

        (f[9],  "Nendran Bananas",           "Fruits",       60.0, "dozen", 150,
         "Kerala's premium Nendran variety — starchy, richly nutritious, distinctive taste. Ideal for banana chips, payasam, and steaming. High potassium.",
         "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=700&q=85", "Kerala Special"),

        (f[5],  "Coorg Mandarin Oranges",    "Fruits",       90.0, "kg",    120,
         "Juicy Coorg mandarins bursting with vitamin C. Thin-skinned, easy-peel, intensely sweet with pleasant tartness. Grown at 3,000 ft elevation.",
         "https://images.unsplash.com/photo-1548103614-609e3e1c7d03?w=700&q=85", ""),

        (f[8],  "Darjeeling Kiwi",           "Fruits",      200.0, "500g",  70,
         "Rare hill-grown kiwi from Darjeeling's cool misty climate. Golden and green varieties. Tangy-sweet, loaded with vitamin C, K and enzymes.",
         "https://images.unsplash.com/photo-1618897996318-5a901fa6ca71?w=700&q=85", "Premium"),

        (f[4],  "Jaisalmer Pomegranate",     "Fruits",       85.0, "piece", 200,
         "Large deep-red pomegranates from Rajasthan's arid farms. Each fruit packed with ruby arils bursting with sweetness. High antioxidant content.",
         "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=700&q=85", ""),

        (f[6],  "Muzaffarpur Shahi Litchi",  "Fruits",      150.0, "500g",  90,
         "GI-tagged Shahi Litchi from Muzaffarpur Bihar — finest litchi in the world. Fragrant, translucent, intensely sweet. Available 3 weeks only per year.",
         "https://images.unsplash.com/photo-1598511726623-d2e9996892f5?w=700&q=85", "GI Tagged"),

        (f[10], "Bikaner Watermelon",        "Fruits",       45.0, "piece", 80,
         "Large sweet watermelons from Rajasthan's desert farms. Deep red flesh, high sugar content. Naturally grown in sandy soil with minimal irrigation.",
         "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=700&q=85", "Seasonal"),

        (f[11], "Andhra Papaya",             "Fruits",       55.0, "piece", 130,
         "Ripe yellow papaya from Andhra Pradesh. Rich in papain enzyme, vitamin C and beta-carotene. Excellent for digestion. Naturally tree-ripened.",
         "https://images.unsplash.com/photo-1526318896980-cf78c088247c?w=700&q=85", ""),

        (f[15-1], "Madurai Grapes",          "Fruits",       95.0, "kg",    110,
         "Sweet seedless grapes from Tamil Nadu's Dindigul district. Thin skin, high sugar, perfect for eating fresh or making juice. No sulfur dioxide treatment.",
         "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=700&q=85", ""),

        (f[9],  "Fresh Green Coconut",       "Fruits",       35.0, "piece", 200,
         "Tender green coconuts from Kerala's coastal farms. Sweet, electrolyte-rich water and soft malai. Cut and delivered within 6 hours of harvest.",
         "https://images.unsplash.com/photo-1559181567-c3190ca9be46?w=700&q=85", "Kerala Fresh"),

        (f[2],  "Guava (Amrood)",            "Fruits",       50.0, "kg",    160,
         "Crisp pink-fleshed guava from Tamil Nadu farms. Exceptionally high vitamin C — 4x more than oranges. Sweet, slightly grainy texture.",
         "https://images.unsplash.com/photo-1536511132770-e5058c7e8c46?w=700&q=85", ""),

        # ═══ GRAINS (10 products) ════════════════════════════════════════════
        (f[3],  "Premium Basmati Rice",      "Grains",      130.0, "kg",    500,
         "Aged 18-month long-grain basmati from Punjab's golden fields. Intoxicating aroma, non-sticky fluffy texture. GI-certified. Ideal for biryani, pulao and kheer.",
         "https://images.unsplash.com/photo-1536304993881-ff86e0c9b31c?w=700&q=85", "Premium"),

        (f[3],  "Yellow Moong Dal",          "Grains",      110.0, "kg",    300,
         "Split and hulled green moong from Punjab farms. Light, easily digestible, quick-cooking. High in protein and folate. Perfect for dal tadka and khichdi.",
         "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=700&q=85", ""),

        (f[6],  "Sona Masoori Rice",         "Grains",       75.0, "kg",    400,
         "Lightweight low-starch Sona Masoori from Bihar. Ideal everyday rice for South Indian meals — idli, dosa and plain rice with sambar. Fresh-season harvest.",
         "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=700&q=85", "Farm Fresh"),

        (f[3],  "Black Urad Dal (Whole)",    "Grains",      130.0, "kg",    200,
         "Whole black lentils from Punjab — the backbone of authentic dal makhani. Creamy when slow-cooked, nutty flavour. High protein and fibre content.",
         "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=700&q=85", ""),

        (f[0],  "Jowar (Sorghum)",           "Grains",       50.0, "kg",    350,
         "Traditional jowar from Telangana — ancient gluten-free grain. High fibre and iron. Perfect for rotis, porridge, and pop sorghum snacks.",
         "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85", "Gluten Free"),

        (f[4],  "Bajra (Pearl Millet)",      "Grains",       45.0, "kg",    280,
         "Iron-rich bajra from Rajasthan's sun-drenched farms. Traditional winter warming grain. Perfect for bajra roti, rabri and bajra khichdi.",
         "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85", ""),

        (f[8],  "Bengal Mustard Seeds",      "Grains",       85.0, "250g",  220,
         "Sharp pungent yellow mustard seeds from West Bengal. Essential for Bengali panch phoron, sarson ka saag, pickles and tempering.",
         "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=700&q=85", ""),

        (f[12], "Punjab Wheat (Gehun)",      "Grains",       42.0, "kg",    600,
         "Hard red wheat from Punjab's fertile plains. High gluten content, ideal for bread, chapati atta and pasta. Freshly harvested, stone-ground quality.",
         "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85", ""),

        (f[15-1], "Ragi (Finger Millet)",    "Grains",       65.0, "kg",    250,
         "High-calcium ragi from Tamil Nadu. Highest calcium of any grain — 344mg per 100g. Gluten-free, low GI, perfect for ragi mudde, porridge and dosas.",
         "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=700&q=85", "Gluten Free"),

        (f[5],  "Toor Dal (Arhar)",          "Grains",       98.0, "kg",    320,
         "Split pigeon peas from Karnataka. The heart of sambar and everyday dal fry. High protein, easy to digest. Freshly cleaned and packed from the farm.",
         "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=700&q=85", "Farm Fresh"),

        # ═══ DAIRY & HONEY (10 products) ════════════════════════════════════
        (f[0],  "A2 Gir Cow Milk",           "Dairy & Honey",  75.0, "litre",  100,
         "Fresh A2 milk from indigenous Gir cows raised on organic feed in open pastures. Rich in omega-3 fatty acids and beta-casein A2 protein. Delivered within 4 hours of milking.",
         "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85", "A2 Certified"),

        (f[9],  "Raw Nilgiri Forest Honey",  "Dairy & Honey", 520.0, "500g",   80,
         "Wild-harvested honey from untouched Nilgiri forest hives. Unprocessed, unheated, no additives. Complex multi-floral profile — each batch unique.",
         "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=700&q=85", "Pure"),

        (f[3],  "Bilona Method Desi Ghee",   "Dairy & Honey", 680.0, "500g",   55,
         "Traditional bilona ghee from Punjab's desi cow milk. Hand-churned, slow-cooked on wood fire. Granular golden ghee with unmistakable nutty aroma.",
         "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=700&q=85", "Bilona Method"),

        (f[5],  "Coorg Wildflower Honey",    "Dairy & Honey", 480.0, "500g",   50,
         "Western Ghats multi-floral honey from Coorg's biodiverse forests. Cold-extracted, raw, unfiltered. Dark amber colour with hints of coffee blossom.",
         "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=700&q=85", "Organic"),

        (f[9],  "Wood-Pressed Coconut Oil",  "Dairy & Honey", 350.0, "litre",  90,
         "Traditional wood-pressed (chekku) virgin coconut oil from Kerala's coastal farms. Authentic coconut aroma, high lauric acid, no hexane extraction.",
         "https://images.unsplash.com/photo-1617132999740-45e4fcda3a62?w=700&q=85", "Cold Pressed"),

        (f[8],  "Bengal Mishti Doi",         "Dairy & Honey",  80.0, "500g",   70,
         "Authentic mishti doi slow-set in traditional earthen pots from West Bengal. Creamy, mildly sweet, pleasantly tangy. Best eaten chilled.",
         "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85", "Traditional"),

        (f[12], "Buffalo Butter (Makhan)",   "Dairy & Honey", 120.0, "200g",   80,
         "Fresh white unsalted butter from Punjab's buffalo milk. High fat content, creamy texture. Churned daily. Best on hot rotis straight off the tawa.",
         "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85", "Farm Fresh"),

        (f[10], "Rajasthani Camel Milk",     "Dairy & Honey", 150.0, "litre",  40,
         "Rare camel milk from Bikaner's traditional herder families. Naturally low in fat, high in insulin-like proteins. Used in traditional Rajasthani medicine.",
         "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85", "Rare"),

        (f[2],  "Nilgiri Tea Honey",         "Dairy & Honey", 420.0, "500g",   45,
         "Honey from bees feeding exclusively on Nilgiri tea blossoms. Light amber, delicate floral notes with subtle earthy undertones. Rare and seasonal.",
         "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=700&q=85", "Artisan"),

        (f[11], "Natu Kodi Egg (Country Egg)","Dairy & Honey", 90.0, "dozen",  120,
         "Free-range country chicken eggs from Andhra Pradesh's open farms. Deep orange yolks, rich flavour. Hens fed on natural grain — no antibiotics.",
         "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=700&q=85", "Free Range"),

        # ═══ SPICES (12 products) ════════════════════════════════════════════
        (f[2],  "Kashmiri Red Chilli Powder","Spices",        220.0, "250g",  300,
         "GI-tagged Kashmiri chillies ground fresh — vivid red colour, mild heat, fruity aromatic profile. The secret to restaurant-quality curries.",
         "https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=700&q=85", "GI Tagged"),

        (f[2],  "Chettinad Pepper Powder",   "Spices",        280.0, "250g",  150,
         "Freshly stone-ground black pepper from Tamil Nadu's Chettinad region. Sharp, pungent, earthy heat. Incomparable flavour versus pre-packaged brands.",
         "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85", "Stone Ground"),

        (f[9],  "Idukki Cardamom (Elaichi)", "Spices",        450.0, "100g",  120,
         "Green cardamom pods from Idukki's high-altitude spice gardens at 5,000 ft. Intensely aromatic, highest essential oil content in India. GI-certified.",
         "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85", "GI Tagged"),

        (f[5],  "Organic Turmeric Fingers",  "Spices",        120.0, "250g",  200,
         "Whole turmeric fingers from Coorg's certified organic farms. Deep orange, curcumin content 5%+ (vs 2-3% in commercial brands). Sun-dried on farm.",
         "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?w=700&q=85", "Organic"),

        (f[2],  "Star Anise (Chakra Phool)", "Spices",        160.0, "100g",  130,
         "Whole star anise from Tamil Nadu — licorice-sweet, warm, heady aroma. Essential for biryani dum, masala chai and meat marinades.",
         "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85", ""),

        (f[3],  "Punjabi Coriander Seeds",   "Spices",         45.0, "250g",  250,
         "Plump, citrusy coriander seeds from Punjab. Freshly harvested and sun-dried on the farm. Sweet, lemony notes with mild earthy undertones.",
         "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85", "Farm Fresh"),

        (f[13], "Karnataka Cumin (Jeera)",   "Spices",         80.0, "250g",  200,
         "Premium cumin seeds from Karnataka's dry farming regions. Warm, earthy, slightly bitter. Freshly harvested with superior volatile oil content.",
         "https://images.unsplash.com/photo-1599909631928-9fe99b2a1ecd?w=700&q=85", ""),

        (f[13], "Cinnamon Bark (Dalchini)",  "Spices",        200.0, "100g",  120,
         "True Ceylon cinnamon (not cassia) from Karnataka's spice gardens. Thin papery layers, delicate sweet-spicy flavour. Lower coumarin than cassia.",
         "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85", "Ceylon"),

        (f[9],  "Cloves (Laung)",            "Spices",        350.0, "100g",  100,
         "Whole cloves from Kerala's spice gardens — intensely aromatic, high eugenol content. Essential for biryani, masala chai and garam masala blends.",
         "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85", ""),

        (f[10], "Fenugreek Seeds (Methi)",   "Spices",         55.0, "250g",  180,
         "Bitter-aromatic fenugreek seeds from Rajasthan. Essential for panch phoron, sambar powder and pickling spice mixes. High in soluble fibre.",
         "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=700&q=85", ""),

        (f[2],  "Bay Leaves (Tej Patta)",    "Spices",         40.0, "50g",   200,
         "Fresh-dried Indian bay leaves (tej patta) from Tamil Nadu's hill farms. Distinct clove-cinnamon aroma unlike Mediterranean bay. Essential for biryani.",
         "https://images.unsplash.com/photo-1600132806608-231446b2e7af?w=700&q=85", ""),

        (f[9],  "Kashmiri Saffron (Kesar)",  "Spices",        650.0, "1g",    30,
         "Authentic Kashmiri Mongra saffron — the world's finest. Deep crimson threads, intense aroma, long-lasting colour. GI-certified from Pampore, Kashmir.",
         "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=700&q=85", "GI Tagged"),
    ]

    pids = []
    for pd in products_data:
        conn.execute(
            "INSERT INTO products(farmer_id,name,category,price,unit,stock,description,image_url,badge) VALUES(?,?,?,?,?,?,?,?,?)",
            pd)
        pids.append(conn.execute("SELECT last_insert_rowid()").fetchone()[0])

    # ── 50 PRE-SEEDED ORDERS ─────────────────────────────────────────────────
    statuses  = ['delivered','delivered','delivered','delivered','confirmed','dispatched','pending','pending']
    p_methods = ['card','upi','netbanking','cod','card','upi','card','netbanking']
    addresses = [
        "Flat 302, Green Valley Apartments, Banjara Hills, Hyderabad - 500034",
        "12-B Koramangala 5th Block, Near Forum Mall, Bengaluru - 560095",
        "901 Shivaji Nagar, Camp Road, Pune - 411005",
        "47 Anna Nagar East, 3rd Avenue, Chennai - 600102",
        "C-14 Vasant Kunj, Sector B, New Delhi - 110070",
        "Flat 5, Park Street Apartments, Kolkata - 700016",
        "Marine Drive Road, Ernakulam, Kochi - 682031",
        "11 Civil Lines, Sitabuldi, Nagpur - 440001",
    ]
    # (cust_idx, prod_idx, qty, stat_idx, pay_idx, date)
    orders_raw = [
        (0, 0,  3, 0, 0, "2024-09-15"), (0, 18, 2, 0, 1, "2024-09-20"),
        (0, 33, 1, 0, 0, "2024-10-01"), (0, 43, 1, 1, 2, "2024-10-10"),
        (0, 8,  2, 0, 1, "2024-10-18"), (0, 1,  2, 0, 0, "2024-11-01"),
        (0, 50, 1, 0, 2, "2024-11-10"), (0, 20, 2, 3, 3, "2024-11-20"),

        (1, 26, 1, 0, 0, "2024-09-12"), (1, 34, 2, 0, 1, "2024-09-25"),
        (1, 44, 1, 0, 0, "2024-10-05"), (1, 55, 1, 4, 2, "2024-10-15"),
        (1, 9,  3, 0, 0, "2024-10-22"), (1, 37, 1, 2, 1, "2024-11-03"),
        (1, 27, 2, 0, 0, "2024-11-15"), (1, 52, 1, 0, 3, "2024-12-01"),

        (2, 2,  2, 0, 1, "2024-09-18"), (2, 4,  5, 0, 0, "2024-09-28"),
        (2, 36, 1, 0, 2, "2024-10-08"), (2, 45, 1, 1, 0, "2024-10-20"),
        (2, 19, 2, 0, 1, "2024-10-30"), (2, 28, 2, 0, 2, "2024-11-08"),
        (2, 41, 1, 3, 3, "2024-11-18"), (2, 57, 1, 0, 0, "2024-12-05"),

        (3, 9,  3, 0, 1, "2024-09-10"), (3, 22, 1, 0, 0, "2024-09-22"),
        (3, 29, 2, 0, 2, "2024-10-02"), (3, 47, 1, 2, 1, "2024-10-12"),
        (3, 10, 2, 0, 0, "2024-10-25"), (3, 54, 1, 0, 1, "2024-11-05"),
        (3, 32, 1, 4, 0, "2024-11-22"), (3, 58, 1, 0, 3, "2024-12-08"),

        (4, 25, 2, 0, 2, "2024-09-08"), (4, 30, 1, 0, 0, "2024-09-20"),
        (4, 38, 1, 1, 1, "2024-10-03"), (4, 46, 3, 0, 2, "2024-10-14"),
        (4, 11, 2, 0, 0, "2024-10-28"), (4, 53, 1, 0, 1, "2024-11-10"),
        (4, 23, 1, 5, 3, "2024-11-25"), (4, 6,  4, 0, 0, "2024-12-10"),

        (5, 3,  4, 0, 1, "2024-09-14"), (5, 17, 1, 0, 0, "2024-10-01"),
        (5, 35, 1, 0, 2, "2024-10-20"), (5, 48, 2, 6, 1, "2024-11-05"),

        (6, 31, 1, 0, 0, "2024-09-16"), (6, 14, 2, 0, 1, "2024-10-06"),
        (6, 56, 1, 0, 2, "2024-11-12"), (6, 42, 3, 7, 0, "2024-12-02"),

        (7, 13, 2, 0, 1, "2024-09-19"), (7, 24, 1, 0, 0, "2024-11-14"),
    ]

    for o in orders_raw:
        ci, pi, qty, si, pmi, date = o
        if pi >= len(pids): pi = pi % len(pids)
        cid    = cids[ci % len(cids)]
        pid    = pids[pi]
        prow   = conn.execute("SELECT price, farmer_id FROM products WHERE id=?", (pid,)).fetchone()
        if not prow: continue
        price  = prow['price']
        fid    = prow['farmer_id']
        total  = price * qty
        status = statuses[si % len(statuses)]
        method = p_methods[pmi % len(p_methods)]
        addr   = addresses[ci % len(addresses)]
        tid    = txn_id()
        cname  = customers_raw[ci % len(customers_raw)][0]
        cphone = customers_raw[ci % len(customers_raw)][3]
        conn.execute(
            """INSERT INTO orders(customer_id,farmer_id,product_id,quantity,unit_price,total,
               status,payment_method,payment_id,delivery_address,delivery_name,delivery_phone,created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cid, fid, pid, qty, price, total, status, method, tid, addr, cname, cphone, date))

    conn.commit()
    conn.close()
    print("✅ Seeded: 15 farmers | 8 customers | 60 products | 50 orders")

# ── LANGUAGE ROUTES ──────────────────────────────────────────────────────────
@app.route('/lang', methods=['GET','POST'])
def lang_select():
    """Language selection page — shown on first visit."""
    if request.method == 'POST':
        chosen = request.form.get('lang', 'en')
        if chosen in LANGUAGES:
            session['lang'] = chosen
            session['lang_chosen'] = True
        return redirect(request.form.get('next', url_for('index')))
    next_url = request.args.get('next', url_for('index'))
    return render_template('lang_select.html', next_url=next_url, **inject_lang())

@app.route('/set_lang/<code>')
def set_lang(code):
    """Quick language switcher from any page."""
    if code in LANGUAGES:
        session['lang'] = code
        session['lang_chosen'] = True
    return redirect(request.referrer or url_for('index'))

# ── ROUTES ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    # Redirect to language selection on very first visit
    if not session.get('lang_chosen'):
        return redirect(url_for('lang_select', next=url_for('index')))
    conn = db()
    products = conn.execute(
        '''SELECT p.*,u.name farmer_name,u.location farmer_loc
           FROM products p JOIN users u ON p.farmer_id=u.id
           ORDER BY RANDOM() LIMIT 8''').fetchall()
    cats = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return render_template('index.html', products=products, cats=cats, **inject_lang())

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = db().execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (request.form['email'], hp(request.form['password']))).fetchone()
        if u:
            session.update(uid=u['id'], name=u['name'], role=u['role'], email=u['email'])
            flash(f"Welcome back, {u['name']}! 🌿", "success")
            return redirect(url_for('dashboard'))
        flash("Incorrect email or password.", "error")
    return render_template('login.html', **inject_lang())

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            conn = db()
            conn.execute(
                "INSERT INTO users(name,email,password,role,phone,location) VALUES(?,?,?,?,?,?)",
                (request.form['name'], request.form['email'], hp(request.form['password']),
                 request.form['role'], request.form.get('phone',''), request.form.get('location','')))
            conn.commit(); conn.close()
            flash("Account created! Please sign in.", "success")
            return redirect(url_for('login'))
        except:
            flash("Email already registered.", "error")
    return render_template('register.html', **inject_lang())

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_req
def dashboard():
    conn = db()
    if session['role'] == 'farmer':
        prods = conn.execute(
            "SELECT * FROM products WHERE farmer_id=? ORDER BY created_at DESC",
            (session['uid'],)).fetchall()
        orders = conn.execute(
            '''SELECT o.*,p.name pname,p.image_url pimg,u.name cname
               FROM orders o JOIN products p ON o.product_id=p.id
               JOIN users u ON o.customer_id=u.id
               WHERE o.farmer_id=? ORDER BY o.created_at DESC''',
            (session['uid'],)).fetchall()
        earn = sum(o['total'] for o in orders if o['status'] == 'delivered')
        conn.close()
        return render_template('farmer_dash.html', prods=prods, orders=orders, earn=earn, **inject_lang())
    else:
        orders = conn.execute(
            '''SELECT o.*,p.name pname,p.image_url pimg,u.name fname
               FROM orders o JOIN products p ON o.product_id=p.id
               JOIN users u ON o.farmer_id=u.id
               WHERE o.customer_id=? ORDER BY o.created_at DESC''',
            (session['uid'],)).fetchall()
        conn.close()
        return render_template('customer_dash.html', orders=orders, **inject_lang())

@app.route('/products')
def products():
    cat = request.args.get('category', '')
    q   = request.args.get('q', '')
    srt = request.args.get('sort', 'new')
    conn = db()
    sql = '''SELECT p.*,u.name farmer_name,u.location farmer_loc
             FROM products p JOIN users u ON p.farmer_id=u.id WHERE p.stock>0'''
    params = []
    if cat: sql += " AND p.category=?";  params.append(cat)
    if q:   sql += " AND p.name LIKE ?"; params.append(f'%{q}%')
    sql += {'new':" ORDER BY p.created_at DESC",
            'asc':" ORDER BY p.price ASC",
            'desc':" ORDER BY p.price DESC"}.get(srt, " ORDER BY p.created_at DESC")
    prods = conn.execute(sql, params).fetchall()
    cats  = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return render_template('products.html', prods=prods, cats=cats, sel=cat, q=q, srt=srt, **inject_lang())

@app.route('/product/<int:pid>')
def product(pid):
    conn = db()
    p = conn.execute(
        '''SELECT p.*,u.name farmer_name,u.phone farmer_phone,u.location farmer_loc
           FROM products p JOIN users u ON p.farmer_id=u.id WHERE p.id=?''', (pid,)).fetchone()
    if not p: conn.close(); return redirect(url_for('products'))
    related = conn.execute(
        "SELECT * FROM products WHERE category=? AND id!=? AND stock>0 LIMIT 4",
        (p['category'], pid)).fetchall()
    conn.close()
    return render_template('product.html', p=p, related=related, **inject_lang())

@app.route('/add_product', methods=['GET','POST'])
@login_req
@farmer_req
def add_product():
    if request.method == 'POST':
        conn = db()
        conn.execute(
            "INSERT INTO products(farmer_id,name,category,price,unit,stock,description,image_url,badge) VALUES(?,?,?,?,?,?,?,?,?)",
            (session['uid'], request.form['name'], request.form['category'],
             float(request.form['price']), request.form['unit'], int(request.form['stock']),
             request.form.get('description',''), request.form.get('image_url',''), request.form.get('badge','')))
        conn.commit(); conn.close()
        flash("Product listed successfully! 🌱", "success")
        return redirect(url_for('dashboard'))
    return render_template('add_product.html', **inject_lang())

@app.route('/delete_product/<int:pid>')
@login_req
@farmer_req
def delete_product(pid):
    conn = db()
    conn.execute("DELETE FROM products WHERE id=? AND farmer_id=?", (pid, session['uid']))
    conn.commit(); conn.close()
    flash("Product removed.", "info")
    return redirect(url_for('dashboard'))

@app.route('/add_cart/<int:pid>', methods=['POST'])
@login_req
def add_cart(pid):
    if session['role'] != 'customer':
        flash("Only customers can add to cart.", "error")
        return redirect(url_for('product', pid=pid))
    qty = int(request.form.get('qty', 1))
    conn = db()
    ex = conn.execute("SELECT * FROM cart WHERE customer_id=? AND product_id=?",
                      (session['uid'], pid)).fetchone()
    if ex: conn.execute("UPDATE cart SET quantity=quantity+? WHERE id=?", (qty, ex['id']))
    else:  conn.execute("INSERT INTO cart(customer_id,product_id,quantity) VALUES(?,?,?)",
                        (session['uid'], pid, qty))
    conn.commit(); conn.close()
    flash("Added to cart!", "success")
    return redirect(url_for('cart'))

@app.route('/cart')
@login_req
def cart():
    conn = db()
    items = conn.execute(
        '''SELECT c.*,p.name,p.price,p.unit,p.image_url,p.stock,u.name farmer_name
           FROM cart c JOIN products p ON c.product_id=p.id
           JOIN users u ON p.farmer_id=u.id WHERE c.customer_id=?''',
        (session['uid'],)).fetchall()
    total = sum(i['price'] * i['quantity'] for i in items)
    conn.close()
    return render_template('cart.html', items=items, total=total, **inject_lang())

@app.route('/remove_cart/<int:cid>')
@login_req
def remove_cart(cid):
    conn = db()
    conn.execute("DELETE FROM cart WHERE id=? AND customer_id=?", (cid, session['uid']))
    conn.commit(); conn.close()
    return redirect(url_for('cart'))

@app.route('/checkout')
@login_req
def checkout():
    conn = db()
    items = conn.execute(
        '''SELECT c.*,p.name,p.price,p.unit,p.image_url,u.name farmer_name
           FROM cart c JOIN products p ON c.product_id=p.id
           JOIN users u ON p.farmer_id=u.id WHERE c.customer_id=?''',
        (session['uid'],)).fetchall()
    if not items: flash("Cart is empty.", "error"); return redirect(url_for('cart'))
    subtotal = sum(i['price'] * i['quantity'] for i in items)
    delivery = 0 if subtotal >= 500 else 40
    tax      = round(subtotal * 0.05, 2)
    grand    = round(subtotal + delivery + tax, 2)
    conn.close()
    return render_template('checkout.html', items=items,
                           subtotal=subtotal, delivery=delivery, tax=tax, grand=grand, **inject_lang())

@app.route('/pay', methods=['POST'])
@login_req
def pay():
    conn = db()
    items = conn.execute(
        '''SELECT c.*,p.price,p.farmer_id,p.stock FROM cart c
           JOIN products p ON c.product_id=p.id WHERE c.customer_id=?''',
        (session['uid'],)).fetchall()
    if not items: flash("Cart is empty.", "error"); return redirect(url_for('cart'))
    method   = request.form.get('method', 'card')
    addr     = request.form.get('address', '')
    dname    = request.form.get('dname', '')
    dphone   = request.form.get('dphone', '')
    tid      = txn_id()
    subtotal = sum(i['price'] * i['quantity'] for i in items)
    delivery = 0 if subtotal >= 500 else 40
    tax      = round(subtotal * 0.05, 2)
    grand    = round(subtotal + delivery + tax, 2)
    for i in items:
        conn.execute(
            '''INSERT INTO orders(customer_id,farmer_id,product_id,quantity,unit_price,total,
               payment_method,payment_id,delivery_address,delivery_name,delivery_phone)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
            (session['uid'], i['farmer_id'], i['product_id'], i['quantity'],
             i['price'], i['price'] * i['quantity'], method, tid, addr, dname, dphone))
        conn.execute("UPDATE products SET stock=stock-? WHERE id=?",
                     (i['quantity'], i['product_id']))
    conn.execute("DELETE FROM cart WHERE customer_id=?", (session['uid'],))
    conn.commit(); conn.close()
    return render_template('success.html', tid=tid, grand=grand, method=method, **inject_lang())

@app.route('/update_order/<int:oid>', methods=['POST'])
@login_req
@farmer_req
def update_order(oid):
    conn = db()
    conn.execute("UPDATE orders SET status=? WHERE id=? AND farmer_id=?",
                 (request.form['status'], oid, session['uid']))
    conn.commit(); conn.close()
    flash("Order updated.", "success")
    return redirect(url_for('dashboard'))

@app.route('/api/cart_count')
def cart_count():
    if 'uid' not in session or session.get('role') != 'customer':
        return jsonify(count=0)
    conn = db()
    n = conn.execute("SELECT COALESCE(SUM(quantity),0) FROM cart WHERE customer_id=?",
                     (session['uid'],)).fetchone()[0]
    conn.close()
    return jsonify(count=n)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
