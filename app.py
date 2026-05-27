import streamlit as st
import requests
from bs4 import BeautifulSoup

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="CR Analiz",
    page_icon="⚔️",
    layout="centered"
)

# Vizual dizayn (Custom CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; background-color: #ffb703; color: black;
        font-weight: bold; border-radius: 8px; border: none; padding: 10px 20px;
    }
    .stButton>button:hover { background-color: #fb8500; color: white; }
    .card {
        padding: 20px; border-radius: 10px; background-color: #161b22;
        margin-bottom: 15px; border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚔️ CR Analiz")
st.write("### 🛡️ Rəqib analizi. Counter qur. Turnir qazan.")

st.markdown("---")

st.markdown("## 🔍 Oyunçu Ara (API Key Tələb Olunmur)")
player_tag = st.text_input("Oyunçu Tag-ini girin (Örn: 2Q9JG2RL):", value="")

if st.button("Analiz Et 🚀"):
    if not player_tag:
        st.warning("⚠️ Zəhmət olmasa bir Oyunçu Tag-i daxil edin.")
    else:
        # Tag-in daxilindəki boşluq və # işarəsini təmizləyirik
        clean_tag = player_tag.replace("#", "").strip().upper()
        
        # Heç bir IP və Key tələb etməyən birbaşa profil linki
        url = f"https://statsroyale.com/profile/{clean_tag}"
        
        with st.spinner("Profil məlumatları və dəstə gətirilir..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Oyunçu adını tapmaq
                    name_element = soup.find("div", {"class": "profileHeader__name"})
                    player_name = name_element.text.strip() if name_element else "Tapılmadı"
                    
                    if player_name == "Tapılmadı":
                        st.error("❌ Oyunçu tapılmadı! Tag-i düzgün yazdığınızdan əmin olun.")
                    else:
                        st.success(f"✅ Oyunçu tapıldı: {player_name}")
                        
                        # Kubok və digər əsas vizual detallar
                        trophy_element = soup.find("div", {"class": "profileHeader__trophies"})
                        trophies = trophy_element.text.strip() if trophy_element else "0"
                        
                        st.markdown(f"""
                        <div class="card">
                            <h3>👤 Oyunçu: {player_name}</h3>
                            <p>🏆 <b>Cari Kubok:</b> {trophies}</p>
                            <p>🆔 <b>Tag:</b> #{clean_tag}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Son istifadə olunan dəstə (Deck)
                        st.subheader("🎴 Son Aktiv Dəstə (Current Deck)")
                        
                        deck_cards = soup.find_all("div", {"class": "profile__card"})
                        
                        if deck_cards:
                            cols = st.columns(4)
                            for idx, card in enumerate(deck_cards[:8]): # Maksimum 8 kart
                                img_tag = card.find("img")
                                card_name = img_tag['alt'] if img_tag and 'alt' in img_tag.attrs else "Kart"
                                
                                with cols[idx % 4]:
                                    st.info(f"**{card_name}**")
                        else:
                            st.info("Aktiv dəstə vizualları yüklənə bilmədi, lakin profil mövcuddur.")
                else:
                    st.error("🚨 Profil platformasından məlumat alınmadı. Bir az sonra yenidən yoxlayın.")
            except Exception as e:
                st.error(f"🚨 Sistem xətası baş verdi: {str(e)}")
