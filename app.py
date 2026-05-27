import streamlit as pd
import streamlit as st
import requests

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="CR Analiz",
    page_icon="⚔️",
    layout="centered"
)

# Custom CSS - Vizual dizayn üçün
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #ffb703;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #fb8500;
        color: white;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #161b22;
        margin-bottom: 15px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

# Başlıq
st.title("⚔️ CR Analiz")
st.write("### 🛡️ Rəqib analizi. Counter qur. Turnir qazan.")

# Statistik vitrin
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🚩 Oturum", value="1")
with col2:
    st.metric(label="👥 Oyunçu", value="1")
with col3:
    st.metric(label="✅ Status", value="Aktiv")

st.markdown("---")

# Dil seçimi
lang = st.selectbox("🌐 Dil / Language", ["Türkçe", "English", "Azərbaycan dili"])

# API Key daxil etmə sahəsi
api_key = st.text_input("🔑 Clash Royale API Key daxil edin:", type="password")

st.markdown("## 🔍 Oyunçu Ara")
player_tag = st.text_input("Oyunçu Tag-ini girin (Örn: #9PJ92RQRD):", value="#")

# Analiz düyməsi və məntiqi
if st.button("Analiz Et 🚀"):
    if player_tag == "#" or not player_tag:
        st.warning("⚠️ Zəhmət olmasa düzgün bir Oyunçu Tag-i daxil edin.")
    elif not api_key:
        st.warning("⚠️ Sorğu göndərmək üçün əvvəlcə API Key daxil etməlisiniz.")
    else:
        # Tag-in başındakı '#' işarəsini URL üçün təmizləyirik (%23 formatına salmaq üçün)
        clean_tag = player_tag.replace("#", "").strip()
        
        # Supercell API birbaşa Streamlit IP-lərini blokladığı üçün proxy URL istifadə edirik
        url = f"https://proxy.royaleapi.dev/v1/players/%23{clean_tag}"
        
        # Xəta verən sətir tamamilə düzəldildi:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        with st.spinner("Məlumatlar gətirilir, gözləyin..."):
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success(Hexlənmiş="✅ Oyunçu tapıldı!")
                    
                    # Kart daxilində əsas məlumatları göstəririk
                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 İstifadəçi adı: {data.get('name', 'Bilinmir')}</h3>
                        <p>🏆 <b>Cari Kubok:</b> {data.get('trophies', 0)}</p>
                        <p>🥇 <b>Maksimum Kubok:</b> {data.get('bestTrophies', 0)}</p>
                        <p>⚔️ <b>Qələbələr:</b> {data.get('wins', 0)} | <b>Məğlubiyyətlər:</b> {data.get('losses', 0)}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Cari gövdə (Deck) analizi
                    st.subheader("🎴 Cari Dəstə (Current Deck)")
                    cards = data.get('currentDeck', [])
                    if cards:
                        cols = st.columns(4)
                        for idx, card in enumerate(cards):
                            with cols[idx % 4]:
                                card_name = card.get('name', '')
                                card_lvl = card.get('level', 1) + (14 - card.get('maxLevel', 14)) # Oyundakı real səviyyəsi
                                st.markdown(f"**{card_name}**\n*(Lvl {card_lvl})*")
                    else:
                        st.info("Bu oyunçunun aktiv dəstə məlumatı tapılmadı.")
                        
                elif response.status_code == 403:
                    st.error("❌ API Key xətası! Daxil etdiyiniz açar (Key) yanlışdır və ya IP icazəsi (0.0.0.0/0) aktiv deyil.")
                elif response.status_code == 404:
                    st.error("❌ Oyunçu tapılmadı! Tag-i düzgün yazdığınızdan əmin olun.")
                else:
                    st.error(f"❌ Xəta baş verdi! Status kodu: {response.status_code}")
                    
            except Exception as e:
                st.error(f"🚨 Sistem xətası: {str(e)}")

st.markdown("<br><hr><center><small>🔒 Tətbiqi idarə edin</small></center>", unsafe_allow_html=True)
