import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")

# BLUE BACKGROUND - Force chestunna
st.markdown("""
<style>
.stApp { background-color: #E3F2FD!important; }
[data-testid="stHeader"] { background-color: #E3F2FD!important; }
h1 { color: #0D47A1!important; }
.stButton>button { background-color: #1976D2!important; color: white!important; border-radius: 12px; width: 100%; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra 💙")
st.write("Telugu lo Raitula Mitra")

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

# WORKING MODELS - try one by one
MODELS = ["meta-llama/llama-4-scout-17b-16e-instruct", "qwen/qwen3-32b", "llama-3.2-90b-vision-preview"]

def ask_groq(prompt, b64):
    for m in MODELS:
        try:
            c = client()
            r = c.chat.completions.create(
                model=m,
                messages=[{"role":"user","content":[
                    {"type":"text","text":prompt},
                    {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                ]}]
            )
            return r.choices[0].message.content + f"\n\n_(model: {m})_"
        except Exception as e:
            continue
    return "Model error - Groq anni models busy, 1 min tarvata try chey"

lang = st.selectbox("Bhasha", ["Telugu","English"])

t1, t2 = st.tabs(["📸 Photo", "🎙️ Voice"])

with t1:
    f1 = st.file_uploader("Photo pettu", type=["jpg","png","jpeg"], key="f1")
    if f1:
        st.image(f1, width=300)
        if st.button("Rogam Enti? 🔍", key="b1"):
            with st.spinner("Chustunna..."):
                st.success(ask_groq(f"Identify crop disease, answer in {lang}. Disease, Reason, Mandu cheppu.", to_b64(f1)))

with t2:
    f2 = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="f2")
    q = st.text_input("Question: mandhu cheppu", key="q1")
    if st.button("Magic ✨", key="b2"):
        if f2 and q:
            with st.spinner("..."):
                st.success(ask_groq(f"Farmer asks: {q}. Photo chusi {lang} lo cheppu.", to_b64(f2)))
