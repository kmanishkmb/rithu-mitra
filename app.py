import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")

# BLUE - strong force
st.markdown("""
<style>
.stApp { background: #E3F2FD!important; }
header { background: #E3F2FD!important; }
h1 { color: #0D47A1!important; }
div.stButton > button { background: #1976D2!important; color: white!important; border-radius: 12px!important; height: 50px!important; font-weight: bold!important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra 💙")

try:
    KEYS = st.secrets["GROQ_KEYS"]
except:
    KEYS = [st.secrets.get("GROQ_API_KEY")]

def get_client(): return Groq(api_key=random.choice(KEYS))

def img_to_b64(f):
    im = Image.open(f)
    im.thumbnail((512,512))
    b = io.BytesIO()
    im.save(b, format="JPEG", quality=60)
    return base64.b64encode(b.getvalue()).decode()

# GROQ OFFICIAL VISION MODELS 2026
VISION_MODEL = "qwen/qwen3-32b" # idhe ippudu working

st.info(f"Model: {VISION_MODEL} | Keys: {len(KEYS)}")

t1, t2 = st.tabs(["📸 Photo", "🎙️ Voice"])

with t1:
    f = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="f1")
    if f:
        st.image(f, width=300)
        if st.button("Rogam Enti? 🔍", key="b1"):
            try:
                c = get_client()
                b64 = img_to_b64(f)
                # QWEN ki special prompt
                resp = c.chat.completions.create(
                    model=VISION_MODEL,
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "You are crop doctor. Identify disease from leaf photo. Answer in Telugu simple. Format: Rogam:, Karanam:, Mandu: "},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                        ]
                    }],
                    max_tokens=1000
                )
                ans = resp.choices[0].message.content
                # Qwen thinking tag teesesey
                if "</think>" in ans:
                    ans = ans.split("</think>")[-1]
                st.success(ans)
                st.balloons()
            except Exception as e:
                st.error(f"Real Error: {e}")
                st.write("Keys check chey - Groq console lo Qwen enabled na?")

with t2:
    f2 = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="f2")
    q = st.text_input("Prashna: mandhu cheppu", key="q2")
    if st.button("Magic ✨", key="b2"):
        if f2:
            try:
                c = get_client()
                b64 = img_to_b64(f2)
                resp = c.chat.completions.create(
                    model=VISION_MODEL,
                    messages=[{"role":"user","content":[
                        {"type":"text","text": f"Q: {q}. Photo chusi Telugu lo cheppu."},
                        {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                    ]}],
                    max_tokens=1000
                )
                ans = resp.choices[0].message.content
                if "</think>" in ans:
                    ans = ans.split("</think>")[-1]
                st.success(ans)
            except Exception as e:
                st.error(f"Real Error: {e}")
