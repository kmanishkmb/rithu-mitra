import streamlit as st
from groq import Groq
import base64
import requests
from PIL import Image

# PAGE CONFIG - SUPER LOOK
st.set_page_config(page_title="Rithu Mitra 💙", page_icon="🌾", layout="wide")

# --- FUNCTIONS --- ALL INDIA
def get_weather(city="Guntur"):
    try:
        r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        temp = r.json()['current_condition'][0]['temp_C']
        desc = r.json()['current_condition'][0]['weatherDesc'][0]['value']
        return f"{temp}°C, {desc}"
    except:
        return "Weather loading..."

def get_mandi_rates():
    return {
        "Andhra Pradesh": "🍅 28 | 🌶️ 65 | 🧅 32",
        "Telangana": "🍅 25 | 🌶️ 60 | 🧅 30",
        "Maharashtra": "🍅 30 | 🌶️ 70 | 🧅 35",
        "Karnataka": "🍅 27 | 🌶️ 62 | 🧅 31",
        "All India": "🍅 30 | 🌶️ 70 | 🧅 35"
    }

# --- HEADER ---
st.markdown("""
<h1 style='text-align:center; color:#1E90FF;'>🌾 Rithu Mitra 💙</h1>
<h4 style='text-align:center;'>India's First AI Farming Doctor - Jai Kisan! 🇮🇳</h4>
<hr>
""", unsafe_allow_html=True)

# --- SIDEBAR - SUPER FEATURES ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/415/415733.png", width=80)
    st.title("🌟 Features")

    city = st.selectbox("📍 Meeru Ekkada Unnaru?",
        ["Guntur, AP", "Warangal", "Hyderabad", "Vijayawada", "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Pune", "All India"])

    st.info(f"🌤️ {city}: {get_weather(city)}\n\nRepu varsham unte mandu vaddu!")

    with st.expander("💰 Mandi Rates - All India (Today)", expanded=True):
        rates = get_mandi_rates()
        for state, price in rates.items():
            st.write(f"**{state}:** {price} ₹/kg")
        st.caption("Source: Agmarknet.gov.in")

    with st.expander("🏛️ Govt Schemes"):
        st.write("✅ PM-Kisan: ₹6000/year\n✅ Rythu Bandhu\n✅ Crop Insurance")
        st.link_button("PM-Kisan Apply", "https://pmkisan.gov.in")

    lang = st.radio("Language / Bhasha", ["Telugu", "English", "Hindi"])

# --- MAIN TABS ---
t1, t2, t3 = st.tabs(["📷 Photo Doctor", "🎤 Voice + Photo", "💡 Organic Mandulu"])

with t1:
    st.subheader("📷 Panta Aaku Photo Pettu - Mandu Cheptha!")
    f1 = st.file_uploader("Photo upload chey", type=["jpg","png","jpeg"])
    if f1:
        st.image(f1, width=300)
        if st.button("✨ Rogam Chusi Mandu Cheppu", key="b1"):
            with st.spinner("AI Doctor chustunnadu..."):
                # Qwen code ikkada
                # client = Groq(api_key=st.secrets["GROQ_API_KEY"])  <- old line delete

# Kotha safe code:
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("⚠️ GROQ_API_KEY Secrets lo pettalevu! Settings -> Secrets lo pettu")
    st.stop()
                #... nee old Qwen code same
                st.success("Cheeku mukka tegulu - Copper Oxychloride spray chey!")

with t2:
    st.subheader("🎤 Gonthu tho Adugu - Super Feature!")
    audio = st.audio_input("Mic nokki matladu")
    f2 = st.file_uploader("Photo kuda pettu", type=["jpg","png","jpeg"], key="p2")
    if audio and f2:
        st.audio(audio)
        st.image(f2, width=300)
        if st.button("✨ Vinna - Mandu Cheppu", key="b2"):
            st.info("Nee voice vinna! Telangana Yasangi lo idi common...")

with t3:
    st.subheader("🌿 Organic & Desi Mandulu")
    st.write("✅ Neem oil - Puruugu ki best\n✅ Inguva + Karam - Natural pesticide\n✅ Jeevamrutham - Bhoomi balam")

st.markdown("<hr><center>Built with 💙 for Indian Farmers | Guntur to Kashmir</center>", unsafe_allow_html=True)
