import streamlit as st
import requests

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

st.markdown("## 🔍 Oyunçu Ara (Açıq Verilənlər Bazası)")
player_tag = st.text_input("Oyunçu Tag-ini girin (Örn: 8LGY0Y8RP):", value="")

if st.button("Analiz Et 🚀"):
    if not player_tag:
        st.warning("⚠️ Zəhmət olmasa bir Oyunçu Tag-i daxil edin.")
    else:
        # Tag təmizləmə
        clean_tag = player_tag.replace("#", "").strip().upper()
        
        # Tamamilə açıq və bloklanmayan API linki
        url = f"https://api.clashroyale.com.es/v1/players/{clean_tag}"
        
        with st.spinner("Məlumatlar bazadan çəkilir, gözləyin..."):
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("✅ Oyunçu tapıldı!")
                    
                    # Profil məlumatları kartı
                    name = data.get('name', 'Bilinmir')
                    trophies = data.get('trophies', 0)
                    best_trophies = data.get('bestTrophies', 0)
                    wins = data.get('wins', 0)
                    losses = data.get('losses', 0)
                    
                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 Oyunçu: {name}</h3>
                        <p>🏆 <b>Cari Kubok:</b> {trophies}</p>
                        <p>🥇 <b>Maksimum Kubok:</b> {best_trophies}</p>
                        <p>⚔️ <b>Qələbə/Məğlubiyyət:</b> {wins}W / {losses}L</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Dəstə (Deck) hissəsi
                    st.subheader("🎴 Cari Aktiv Dəstə")
                    cards = data.get('currentDeck', [])
                    
                    if cards:
                        cols = st.columns(4)
                        for idx, card in enumerate(cards):
                            card_name = card.get('name', 'Kart')
                            card_lvl = card.get('level', 1)
                            with cols[idx % 4]:
                                st.info(f"**{card_name}**\n*(Lvl {card_lvl})*")
                    else:
                        st.info("Aktiv dəstə məlumatı tapılmadı.")
                        
                elif response.status_code == 404:
                    st.error("❌ Oyunçu tapılmadı! Tag-i düzgün yazdığınızdan əmin olun.")
                else:
                    st.error(f"🚨 Sistem hazırda cavab vermir (Status: {response.status_code}).")
                    
            except Exception as e:
                st.error(f"🚨 Bağlantı xətası: {str(e)}")
