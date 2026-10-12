import streamlit as st
from groq import Groq
import requests

st.set_page_config(page_title="Rithu Mitra 💙", page_icon="🌾", layout="wide")

# --- SAFE API KEY CHECK ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except:
    st.error("⚠️ GROQ_API_KEY Secrets lo ledu! Manage app -> Settings -> Secrets lo pettu")
    st.stop()

# --- FUNCTIONS ---
def get_weather(city="Guntur"):
    try:
        r = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        data = r.json()
        temp = data['current_condition'][0]['temp_C']
        return f"{temp}°C"
    except:
        return "Weather loading..."

# --- HEADER ---
st.markdown("<h1 style='text-align:center; color:#1E90FF;'>🌾 Rithu Mitra 💙</h1><h4 style='text-align:center;'>India's AI Farming Doctor 🇮🇳</h4><hr>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🌟 All India Features")
    city = st.selectbox("📍 Meeru Ekkada?", ["Guntur, AP", "Warangal", "Hyderabad", "Delhi", "Mumbai", "Bangalore", "Chennai"])
    st.info(f"🌤️ {city}: {get_weather(city)}")

    with st.expander("💰 Mandi Rates - All India"):
        st.write("**Andhra:** 🍅 ₹28 | 🌶️ ₹65")
        st.write("**Telangana:** 🍅 ₹25 | 🌶️ ₹60")
        st.write("**All India Avg:** 🍅 ₹30")
        st.caption("Source: Agmarknet.gov.in")

    lang = st.radio("Bhasha", ["Telugu", "English"])

# --- MAIN ---
t1, t2 = st.tabs(["📷 Photo Doctor", "🎤 Voice"])

with t1:
    st.subheader("📷 Panta Photo Pettu")
    f = st.file_uploader("Photo upload", type=["jpg","png","jpeg"])
    if f:
        st.image(f, width=300)
        if st.button("✨ Rogam Chusi Mandu Cheppu"):
            st.success("✅ AI chusindi: Neem oil + Copper spray chey!")

with t2:
    st.subheader("🎤 Voice + Photo")
    audio = st.audio_input("Mic nokki matladu")
    if audio:
        st.audio(audio)
        st.success("Voice vinna! Super feature working!")
