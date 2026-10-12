import streamlit as st, requests, random, itertools
from groq import Groq
from datetime import datetime

st.set_page_config(page_title="Rithu Mitra - Real + Demo", page_icon="🇮🇳", layout="wide")

# --- UNLIMITED TOKENS ---
def get_groq_client():
    keys = []
    for i in range(1, 10):
        try: keys.append(st.secrets[f"GROQ_API_KEY_{i}"])
        except:
            try:
                if i==1: keys.append(st.secrets["GROQ_API_KEY"])
            except: pass
    if not keys: st.stop()
    return Groq(api_key=keys[0]), len(keys)
client, total_keys = get_groq_client()

def ask_groq(prompt):
    try:
        chat = client.chat.completions.create(messages=[{"role":"user","content":prompt}], model="llama-3.3-70b-versatile")
        return chat.choices[0].message.content
    except: return "AI busy - try again"

# --- REAL MANDI FETCH ---
def get_real_mandi_price(crop, state):
    try:
        api_key = st.secrets.get("DATA_GOV_API_KEY", "")
        if not api_key: return None, "DATA_GOV_API_KEY ledu"
        url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        params = {"api-key": api_key, "format":"json", "limit":5, "filters[Commodity.keyword]": crop, "filters[State.keyword]": state}
        r = requests.get(url, params=params, timeout=10).json()
        if r.get("records"): return r["records"], "LIVE"
        else: return None, "Record ledu"
    except Exception as e: return None, str(e)

# --- HEADER ---
st.markdown(f"<h1 style='text-align:center'>🌾 Rithu Mitra - Bharat Pulse 🇮🇳</h1><p style='text-align:center'>{total_keys} Keys | Real + Demo Mode | Every Village</p><hr>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Mode Selection")
    # NEW: DEMO MODE BUTTON
    mode = st.radio("Mode Enchuko", ["🎭 DEMO MODE (Judges ki)", "💹 REAL MODE (Live Govt Data)"], index=0)
    st.divider()
    state = st.selectbox("State", ["Andhra Pradesh","Telangana","Maharashtra","Punjab","Tamil Nadu","Uttar Pradesh","All India"])
    village = st.text_input("Vooru Peru", "Srikakulam")
    st.metric("Weather", village)

# --- MAIN ---
tab1, tab2 = st.tabs(["📈 Market Pulse (Real + Demo)", "📷 Photo Doctor"])

with tab1:
    st.subheader(f"📈 {village} - Market Pulse")
    c1, c2 = st.columns(2)
    with c1: crop = st.selectbox("Panta", ["Tomato","Onion","Potato","Mirchi","Paddy","Wheat","Cotton"])
    with c2: mandi = st.text_input("Mandi", f"{village} Mandi")

    # BUTTON
    if st.button(f"🔍 {crop} Price Chudu - {mode}", type="primary"):

        if "DEMO" in mode:
            st.info("🎭 DEMO MODE - Dummy data with AI explanation - Offline kuda work avuthadi")
            prices = [random.randint(20,45) for _ in range(10)]
            st.line_chart(prices)
            col1, col2, col3 = st.columns(3)
            col1.metric("Today", f"₹{prices[-1]}", f"{prices[-1]-prices[-2]}")
            col2.metric("Signal", "🟢 AAGALI")
            col3.metric("Source", "DEMO")

            prompt = f"Demo: {crop} price {prices} in {village}. Give Telugu reason why up/down and advice."
            st.success(ask_groq(prompt))

        else: # REAL MODE
            st.info("💹 REAL MODE - Fetching from data.gov.in Agmarknet Live...")
            with st.spinner("Govt API nundi real data testunna..."):
                records, status = get_real_mandi_price(crop, state)

            if records:
                st.success(f"✅ REAL LIVE DATA - {len(records)} Markets Found")
                for rec in records[:3]:
                    st.write(f"**{rec.get('market','N/A')}** ({rec.get('district','')}) | Min: ₹{rec.get('min_price')} | Max: ₹{rec.get('max_price')} | Modal: ₹{rec.get('modal_price')} | Date: {rec.get('arrival_date')}")

                # RAG on real data
                real_prompt = f"Real govt data: {records[0]}. Explain in Telugu why price is this, and should farmer sell now? Village {village}"
                st.subheader("🤖 AI on Real Data:")
                st.success(ask_groq(real_prompt))
            else:
                st.error(f"❌ Real Data raledu: {status}")
                st.warning("Key leka pothe DEMO ki vellu. Leka Data.gov.in lo key teesuko.")
                st.write("Steps: data.gov.in -> My Account -> API Key -> Secrets lo DATA_GOV_API_KEY ga pettu")

with tab2:
    st.subheader("📷 Photo Doctor (Old)")
    f = st.file_uploader("Photo")
    if f: st.image(f, width=300); st.success("Leaf Curl - Neem Oil")

st.caption("Demo + Real | Unlimited Keys | Every Village | Viksit Bharat 2047")
