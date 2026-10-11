import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾", layout="centered")

# BLUE THEME - FINAL
st.markdown("""
<style>
.stApp { background-color: #90CAF9!important; }
header { background-color: #90CAF9!important; }
h1 { color: #0D47A1!important; text-align:center; font-weight:900!important; }
h2, h3 { color: #0D47A1!important; }
.stButton button { background-color: #0D47A1!important; color: white!important; border-radius: 15px!important; width:100%!important; height:55px!important; font-weight:bold!important; font-size:18px!important; }
.stTabs [data-baseweb="tab"] { background-color: white!important; border-radius: 10px!important; }
div[data-testid="stSuccess"] { background-color: #E8F5E9!important; border: 2px solid #2E7D32!important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra 💙")
st.markdown("<center><b style='color:#0D47A1;'>రైతు మిత్రుడు - Groq AI తో</b></center>", unsafe_allow_html=True)
st.divider()

try:
    KEYS = st.secrets["GROQ_KEYS"]
except:
    KEYS = [st.secrets.get("GROQ_API_KEY")]

def client(): return Groq(api_key=random.choice(KEYS))

def to_b64(f):
    img = Image.open(f)
    img.thumbnail((600,600))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()

MODEL = "qwen/qwen3.8-27b"

lang = st.selectbox("🌐 Bhasha / Language", ["Telugu","English","Hindi"], index=0)

t1, t2 = st.tabs(["📸 Photo Doctor", "🎙️ Voice + Photo"])

with t1:
    f = st.file_uploader("📷 Panta Aaku Photo Pettu", type=["jpg","png","jpeg"], key="p1")
    if f:
        st.image(f, caption="Nee Panta", width=350)
        if st.button("🔍 Rogam Enti? Cheppu", key="b1", use_container_width=True):
            with st.spinner("👨‍🌾 Rithu Mitra chustondi... 5 sec"):
                try:
                    c = client()
                    b64 = to_b64(f)
                    prompt = f"""
You are expert Telugu farmer doctor from Warangal with 20 years experience.
Task: Look at leaf photo and give practical advice.

Language: {lang} (pure Telugu, simple village style, no English mix if Telugu)

RULES - DO NOT REPEAT SAME SENTENCE:
- Give exact disease name
- Karanam: 2 lines only
- Mandu: 3 BEST market medicines with EXACT dose. Example: Saaf (Mancozeb) 2gm per liter, Karathane 1ml/L, Sulfex 80WP 2.5gm/L
- Inti Chitka: Neem oil 5ml + 1 liter water
- Jagrathalu: 2 points

Format exactly like this in {lang}:
🌿 Rogam:
🦠 Karanam:
💊 Mandu:
1....
2....
3....
🏠 Inti Chitka:
🛡️ Jagrathalu:

Be helpful, not repetitive.
"""
                    res = c.chat.completions.create(
                        model=MODEL,
                        messages=[{"role":"user","content":[
                            {"type":"text","text": prompt},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                        ]}],
                        max_tokens=1500,
                        temperature=0.3
                    )
                    ans = res.choices[0].message.content
                    if "</think>" in ans: ans = ans.split("</think>")[-1].strip()
                    st.success(ans)
                    st.balloons()
                    st.caption(f"✅ Powered by {MODEL} | {len(KEYS)} keys active")
                except Exception as e:
                    st.error(f"Error: {e}")

with t2:
    f2 = st.file_uploader("📷 Photo", type=["jpg","png","jpeg"], key="p2")
    q = st.text_input("🎤 Prashna Adugu: (ex: mandhu entha vadali?)", placeholder="mandhu cheppu annayya")
    if st.button("✨ Magic Answer", key="b2", use_container_width=True):
        if f2 and q:
            with st.spinner("..."):
                try:
                    c = client()
                    b64 = to_b64(f2)
                    res = c.chat.completions.create(
                        model=MODEL,
                        messages=[{"role":"user","content":[
                            {"type":"text","text": f"Farmer question: {q}. Answer in {lang} simple. Give medicine with dose. Don't repeat."},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                        ]}],
                        max_tokens=1000,
                        temperature=0.3
                    )
                    ans = res.choices[0].message.content
                    if "</think>" in ans: ans = ans.split("</think>")[-1].strip()
                    st.success(ans)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Photo + Question rendu pettu Manish!")

st.divider()
st.markdown("<center>💙 Made for Telangana Farmers | Rithu Mitra</center>", unsafe_allow_html=True)
