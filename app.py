import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")

# BLUE THEME
st.markdown("""
<style>
.stApp { background-color: #90CAF9!important; }
header { background-color: #90CAF9!important; }
h1 { color: #0D47A1!important; text-align:center; }
.stButton button { background-color: #0D47A1!important; color: white!important; border-radius: 15px!important; width:100%!important; height:55px!important; font-weight:bold!important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra 💙")
st.markdown("<center><b style='color:#0D47A1;'>Groq Qwen3.8 - Unlimited</b></center>", unsafe_allow_html=True)

try:
    KEYS = st.secrets["GROQ_KEYS"]
    st.success(f"✅ {len(KEYS)} Keys Loaded")
except:
    KEYS = [st.secrets.get("GROQ_API_KEY")]

def client(): return Groq(api_key=random.choice(KEYS))

def to_b64(f):
    img = Image.open(f)
    img.thumbnail((512,512))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60)
    return base64.b64encode(buf.getvalue()).decode()

MODEL = "qwen/qwen3.8-27b" # NEE ACCOUNT LO UNNA OKKATE VISION MODEL

lang = st.selectbox("Bhasha", ["Telugu","English"], key="lang")

t1, t2 = st.tabs(["📸 Photo Doctor", "🎙️ Voice + Photo"])

with t1:
    f = st.file_uploader("Panta photo", type=["jpg","png","jpeg"], key="p1")
    if f:
        st.image(f, width=300)
        if st.button("Rogam Enti? 🔍", key="b1"):
            with st.spinner("Qwen 3.8 chustondi..."):
                try:
                    c = client()
                    b64 = to_b64(f)
                    res = c.chat.completions.create(
                        model=MODEL,
                        messages=[{"role":"user","content":[
                            {"type":"text","text": f"You are crop doctor. Identify disease from leaf. Answer in {lang}. Format: Rogam:, Karanam:, Mandu:, Jagrathalu:. Simple Telugu."},
                            {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                        ]}],
                        max_tokens=1200
                    )
                    ans = res.choices[0].message.content
                    if "</think>" in ans:
                        ans = ans.split("</think>")[-1].strip()
                    if "<think>" in ans:
                        ans = ans.split("</think>")[-1] if "</think>" in ans else ans
                    st.success(ans)
                    st.balloons()
                    st.caption(f"✅ Model: {MODEL}")
                except Exception as e:
                    st.error(f"Error: {e}")

with t2:
    f2 = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="p2")
    q = st.text_input("Prashna: mandhu cheppu?", key="q2")
    if st.button("Magic ✨", key="b2"):
        if f2 and q:
            try:
                c = client()
                b64 = to_b64(f2)
                res = c.chat.completions.create(
                    model=MODEL,
                    messages=[{"role":"user","content":[
                        {"type":"text","text": f"Q: {q}. Answer in {lang}."},
                        {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                    ]}],
                    max_tokens=1000
                )
                ans = res.choices[0].message.content
                if "</think>" in ans: ans = ans.split("</think>")[-1].strip()
                st.success(ans)
            except Exception as e:
                st.error(f"Error: {e}")
