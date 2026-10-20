import streamlit as st
import pandas as pd
import hashlib
import time
from datetime import datetime

# ============================================
# KONFIGURASI HALAMAN
# ============================================
st.set_page_config(
    page_title="ShopeeClone - Belanja Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS CUSTOM (Tampilan mirip Shopee)
# ============================================
st.markdown("""
<style>
    /* Header oranye khas Shopee */
    .main-header {
        background: linear-gradient(90deg, #ee4d2d 0%, #ff7337 100%);
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
    }
    .main-header h1 { color: white; margin: 0; font-size: 28px; }
    .main-header p { color: #ffe5dc; margin: 5px 0 0 0; font-size: 13px; }

    /* Card produk */
    .product-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(238,77,45,0.2);
    }
    .product-name {
        font-size: 14px;
        font-weight: 600;
        color: #222;
        height: 40px;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .product-price {
        color: #ee4d2d;
        font-size: 18px;
        font-weight: 700;
    }
    .product-old-price {
        color: #999;
        font-size: 12px;
        text-decoration: line-through;
        margin-left: 6px;
    }
    .product-rating { color: #ffce3d; font-size: 13px; }
    .product-sold { color: #888; font-size: 12px; }

    /* Tombol beli */
    .stButton > button {
        background: #ee4d2d;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: #d73211;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ee4d2d 0%, #ff7337 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input {
        color: #222 !important;
        background: white !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: white;
        color: #ee4d2d;
        border: 2px solid white;
    }

    /* Badge kategori */
    .badge {
        display: inline-block;
        background: #ee4d2d;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 11px;
        margin: 2px;
    }
    .badge-green { background: #26aa99; }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "cart" not in st.session_state:
    st.session_state.cart = []
if "hacked" not in st.session_state:
    st.session_state.hacked = False
if "page" not in st.session_state:
    st.session_state.page = "home"

# ============================================
# DATABASE USER (demo - gunakan hash di produksi)
# ============================================
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

USERS_DB = {
    "admin": hash_pw("admin123"),
    "user1": hash_pw("password"),
}

# ============================================
# DATA PRODUK
# ============================================
@st.cache_data
def get_products():
    data = [
        # PAKAIAN
        {"id": 1, "nama": "Kaos Polos Premium Cotton", "kategori": "Pakaian",
         "harga": 89000, "harga_asli": 150000, "rating": 4.8, "terjual": 1200,
         "emoji": "👕", "stok": 50},
        {"id": 2, "nama": "Kemeja Flanel Kotak-Kotak", "kategori": "Pakaian",
         "harga": 159000, "harga_asli": 220000, "rating": 4.7, "terjual": 890,
         "emoji": "👔", "stok": 30},
        {"id": 3, "nama": "Jaket Hoodie Oversize", "kategori": "Pakaian",
         "harga": 199000, "harga_asli": 350000, "rating": 4.9, "terjual": 2500,
         "emoji": "🧥", "stok": 25},
        {"id": 4, "nama": "Celana Jeans Slim Fit", "kategori": "Pakaian",
         "harga": 175000, "harga_asli": 280000, "rating": 4.6, "terjual": 750,
         "emoji": "👖", "stok": 40},

        # SEPATU
        {"id": 5, "nama": "Sneakers Running Sport", "kategori": "Sepatu",
         "harga": 289000, "harga_asli": 450000, "rating": 4.8, "terjual": 1800,
         "emoji": "👟", "stok": 35},
        {"id": 6, "nama": "Sepatu Formal Kulit Premium", "kategori": "Sepatu",
         "harga": 399000, "harga_asli": 650000, "rating": 4.7, "terjual": 420,
         "emoji": "👞", "stok": 20},
        {"id": 7, "nama": "Sandal Slide Kasual", "kategori": "Sepatu",
         "harga": 85000, "harga_asli": 120000, "rating": 4.5, "terjual": 3100,
         "emoji": "🩴", "stok": 100},
        {"id": 8, "nama": "Boots High Ankle", "kategori": "Sepatu",
         "harga": 320000, "harga_asli": 500000, "rating": 4.6, "terjual": 350,
         "emoji": "🥾", "stok": 15},

        # POMPA/SANDAL & AKSESORIS
        {"id": 9, "nama": "Pompa Sepeda Portable", "kategori": "Pompa",
         "harga": 129000, "harga_asli": 180000, "rating": 4.7, "terjual": 650,
         "emoji": "🖐️", "stok": 45},
        {"id": 10, "nama": "Pompa Air Elektrik Mini", "kategori": "Pompa",
         "harga": 249000, "harga_asli": 380000, "rating": 4.6, "terjual": 280,
         "emoji": "💧", "stok": 22},

        # TABLET
        {"id": 11, "nama": "Tablet Android 10 inch 128GB", "kategori": "Tablet",
         "harga": 2499000, "harga_asli": 3200000, "rating": 4.8, "terjual": 540,
         "emoji": "📱", "stok": 12},
        {"id": 12, "nama": "Tablet Pro 11 inch 256GB", "kategori": "Tablet",
         "harga": 5999000, "harga_asli": 7500000, "rating": 4.9, "terjual": 210,
         "emoji": "💻", "stok": 8},
        {"id": 13, "nama": "Tablet Kids 7 inch", "kategori": "Tablet",
         "harga": 899000, "harga_asli": 1200000, "rating": 4.5, "terjual": 870,
         "emoji": "🖥️", "stok": 30},

        # PERALATAN LAIN
        {"id": 14, "nama": "Headphone Bluetooth Wireless", "kategori": "Elektronik",
         "harga": 350000, "harga_asli": 550000, "rating": 4.7, "terjual": 2200,
         "emoji": "🎧", "stok": 55},
        {"id": 15, "nama": "Jam Tangan Digital Sport", "kategori": "Elektronik",
         "harga": 425000, "harga_asli": 680000, "rating": 4.6, "terjual": 940,
         "emoji": "⌚", "stok": 28},
        {"id": 16, "nama": "Powerbank 20000mAh Fast Charging", "kategori": "Elektronik",
         "harga": 189000, "harga_asli": 299000, "rating": 4.8, "terjual": 3500,
         "emoji": "🔋", "stok": 75},
        {"id": 17, "nama": "Tas Ransel Anti Air", "kategori": "Aksesoris",
         "harga": 145000, "harga_asli": 220000, "rating": 4.6, "terjual": 1100,
         "emoji": "🎒", "stok": 40},
        {"id": 18, "nama": "Kacamata Anti Radiasi", "kategori": "Aksesoris",
         "harga": 99000, "harga_asli": 150000, "rating": 4.5, "terjual": 680,
         "emoji": "🕶️", "stok": 60},
        {"id": 19, "nama": "Botol Minum Stainless 1L", "kategori": "Peralatan",
         "harga": 79000, "harga_asli": 130000, "rating": 4.7, "terjual": 1500,
         "emoji": "🍶", "stok": 90},
        {"id": 20, "nama": "Lampu LED Meja Belajar", "kategori": "Peralatan",
         "harga": 115000, "harga_asli": 175000, "rating": 4.6, "terjual": 780,
         "emoji": "💡", "stok": 50},
    ]
    return pd.DataFrame(data)

# ============================================
# FUNGSI HACKER DETECTION (ASCII ART)
# ============================================
def tampilkan_hacker_screen():
    ascii_art = r"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  < Happy Hacking! >                                      ║
║  ═══════════════════                                     ║
║          \   ^__^                                        ║
║           \  (oo)\_______                                ║
║              (__)\       )\/\                            ║
║                  ||----w |                               ║
║                  ||     ||                               ║
║                                                          ║
║  ⚠️  UNAUTHORIZED ACCESS DETECTED ⚠️                     ║
║                                                          ║
║  IP Address  : 192.168.xxx.xxx                           ║
║  Timestamp   : {ts}                            ║
║  Status      : BLOCKED                                   ║
║                                                          ║
║  "Your hacking attempt has been logged and reported."    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
""".format(ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    st.markdown("""
    <style>
        .hacker-screen {
            background: #0a0a0a;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            padding: 40px;
            border-radius: 10px;
            border: 2px solid #00ff41;
            text-align: center;
            box-shadow: 0 0 30px rgba(0,255,65,0.5);
        }
        .hacker-screen pre {
            color: #00ff41;
            text-align: left;
            display: inline-block;
            font-size: 13px;
            line-height: 1.4;
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        .cursor { animation: blink 1s infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hacker-screen">
        <pre>{ascii_art}</pre>
        <p class="cursor">█</p>
        <p style="color:#ff4444; font-size:16px; margin-top:20px;">
            🔒 AKSES DITOLAK — SISTEM MENGUNCI AKUN ANDA 🔒
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.error("⚠️ Terdeteksi percobaan akses tidak sah! Aktivitas Anda telah dicatat.")
    if st.button("🔄 Kembali ke Halaman Login"):
        st.session_state.hacked = False
        st.session_state.logged_in = False
        st.rerun()

# ============================================
# DETEKSI INJEKSI / HACKING
# ============================================
HACK_KEYWORDS = [
    "' or '1'='1", "1=1", "drop table", "union select",
    "<script", "javascript:", "onerror=", "onload=",
    "../", "etc/passwd", "cmd.exe", "eval(", "exec(",
    "select * from", "insert into", "delete from",
    "admin'--", "'; --", "sqlmap", "nmap", "metasploit",
    "hack", "exploit", "payload", "xss", "csrf"
]

def deteksi_hacking(input_str):
    if not input_str:
        return False
    low = input_str.lower()
    for kw in HACK_KEYWORDS:
        if kw in low:
            return True
    # Deteksi simbol mencurigakan berlebihan
    if low.count("'") >= 2 or low.count("--") >= 1 or low.count(";") >= 2:
        return True
    return False

# ============================================
# HALAMAN LOGIN
# ============================================
def halaman_login():
    if st.session_state.hacked:
        tampilkan_hacker_screen()
        return

    st.markdown("""
    <div class="main-header">
        <h1>🛍️ ShopeeClone</h1>
        <p>Belanja Online Terpercaya — Gratis Ongkir se-Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 Login / Daftar")
        tab1, tab2 = st.tabs(["Login", "Daftar"])

        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("🚀 Masuk", use_container_width=True):
                # DETEKSI HACKING
                if deteksi_hacking(username) or deteksi_hacking(password):
                    st.session_state.hacked = True
                    st.rerun()

                if username in USERS_DB and USERS_DB[username] == hash_pw(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Selamat datang, {username}!")
                    time.sleep(0.6)
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")

            st.info("💡 Demo: `admin` / `admin123` atau `user1` / `password`")

        with tab2:
            new_user = st.text_input("Username Baru", key="reg_user")
            new_pass = st.text_input("Password Baru", type="password", key="reg_pass")
            new_pass2 = st.text_input("Konfirmasi Password", type="password", key="reg_pass2")

            if st.button("📝 Daftar", use_container_width=True):
                if deteksi_hacking(new_user) or deteksi_hacking(new_pass):
                    st.session_state.hacked = True
                    st.rerun()

                if not new_user or not new_pass:
                    st.warning("⚠️ Isi semua field!")
                elif new_pass != new_pass2:
                    st.error("❌ Password tidak cocok!")
                elif new_user in USERS_DB:
                    st.error("❌ Username sudah dipakai!")
                else:
                    USERS_DB[new_user] = hash_pw(new_pass)
                    st.success("✅ Registrasi berhasil! Silakan login.")

# ============================================
# SIDEBAR USER
# ============================================
def sidebar_user():
    with st.sidebar:
        st.markdown(f"### 👤 Halo, **{st.session_state.username}**!")
        st.markdown("---")

        # Pencarian
        search = st.text_input("🔍 Cari Produk", key="search_input")

        # Filter kategori
        kategori = st.multiselect(
            "📂 Kategori",
            ["Pakaian", "Sepatu", "Pompa", "Tablet", "Elektronik", "Aksesoris", "Peralatan"],
            default=[]
        )

        # Range harga
        harga_max = st.slider("💰 Harga Maksimal (Rp)", 0, 8000000, 8000000, step=50000)

        # Urutkan
        urut = st.selectbox("🔃 Urutkan", ["Relevan", "Termurah", "Termahal", "Terlaris", "Rating"])

        st.markdown("---")
        st.markdown(f"### 🛒 Keranjang ({len(st.session_state.cart)})")

        if st.session_state.cart:
            total = 0
            for i, item in enumerate(st.session_state.cart):
                st.markdown(f"{item['emoji']} **{item['nama'][:20]}...**  \n"
                            f"Rp {item['harga']:,} x{item['qty']}")
                total += item['harga'] * item['qty']
            st.markdown(f"**Total: Rp {total:,}**")
            if st.button("🗑️ Kosongkan", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        else:
            st.caption("Keranjang kosong")

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.cart = []
            st.rerun()

    return search, kategori, harga_max, urut

# ============================================
# CARD PRODUK
# ============================================
def render_card(prod):
    diskon = int((1 - prod["harga"] / prod["harga_asli"]) * 100)
    with st.container(border=True):
        st.markdown(f"<div style='text-align:center; font-size:64px;'>{prod['emoji']}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"<div class='product-name'>{prod['nama']}</div>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<span class='badge'>-{diskon}%</span>"
            f"<span class='product-price'>Rp {prod['harga']:,}</span>"
            f"<span class='product-old-price'>Rp {prod['harga_asli']:,}</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span class='product-rating'>⭐ {prod['rating']}</span> "
            f"<span class='product-sold'>| {prod['terjual']:,} terjual</span>",
            unsafe_allow_html=True
        )
        if st.button(f"➕ Keranjang", key=f"add_{prod['id']}", use_container_width=True):
            # cek sudah ada
            found = False
            for item in st.session_state.cart:
                if item["id"] == prod["id"]:
                    item["qty"] += 1
                    found = True
                    break
            if not found:
                st.session_state.cart.append({
                    "id": prod["id"], "nama": prod["nama"],
                    "harga": prod["harga"], "emoji": prod["emoji"], "qty": 1
                })
            st.success("✅ Ditambahkan!")
            st.rerun()

# ============================================
# HALAMAN HOME
# ============================================
def halaman_home():
    search, kategori, harga_max, urut = sidebar_user()

    # HEADER
    st.markdown("""
    <div class="main-header">
        <h1>🛍️ ShopeeClone</h1>
        <p>⚡ Flash Sale Hari Ini — Diskon hingga 70%! | 🚚 Gratis Ongkir</p>
    </div>
    """, unsafe_allow_html=True)

    # Banner promo
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div style='background:linear-gradient(135deg,#ff6b6b,#ee4d2d);
                    color:white;padding:20px;border-radius:10px;text-align:center'>
                    <h3>🔥 FLASH SALE</h3><p>Diskon s.d 70%</p></div>""",
                    unsafe_allow_html=True)
    with c2:
        st.markdown("""<div style='background:linear-gradient(135deg,#4ecdc4,#26aa99);
                    color:white;padding:20px;border-radius:10px;text-align:center'>
                    <h3>🚚 GRATIS ONGKIR</h3><p>Min. belanja Rp 0</p></div>""",
                    unsafe_allow_html=True)
    with c3:
        st.markdown("""<div style='background:linear-gradient(135deg,#ffce3d,#ffa500);
                    color:white;padding:20px;border-radius:10px;text-align:center'>
                    <h3>💳 CASHBACK</h3><p>s.d 20%</p></div>""",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FILTER DATA
    df = get_products()
    if search:
        df = df[df["nama"].str.contains(search, case=False, na=False)]
    if kategori:
        df = df[df["kategori"].isin(kategori)]
    df = df[df["harga"] <= harga_max]

    # URUTKAN
    if urut == "Termurah":
        df = df.sort_values("harga")
    elif urut == "Termahal":
        df = df.sort_values("harga", ascending=False)
    elif urut == "Terlaris":
        df = df.sort_values("terjual", ascending=False)
    elif urut == "Rating":
        df = df.sort_values("rating", ascending=False)

    # TAMPILKAN PRODUK
    st.subheader(f"📦 {len(df)} Produk Ditemukan")

    if len(df) == 0:
        st.warning("😔 Tidak ada produk yang cocok dengan filter Anda.")
        return

    # Grid 4 kolom
    cols_per_row = 4
    rows = (len(df) + cols_per_row - 1) // cols_per_row
    idx = 0
    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            if idx < len(df):
                with cols[c]:
                    render_card(df.iloc[idx].to_dict())
                idx += 1

    # FOOTER
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#888;padding:20px'>"
        "© 2025 ShopeeClone — Demo Project untuk Streamlit<br>"
        "Dibuat dengan ❤️ menggunakan Streamlit</div>",
        unsafe_allow_html=True
    )

# ============================================
# MAIN
# ============================================
def main():
    if not st.session_state.logged_in:
        halaman_login()
    else:
        halaman_home()

if __name__ == "__main__":
    main()