import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra UNLIMITED", page_icon="🌾", layout="centered")

# --- STYLE - Vercel laga kanipinchadaniki ---
st.markdown("""
<style>
.stButton>button {background: #16a34a; color: white; border-radius: 12px; width: 100%; padding: 12px; font-weight: bold;}
.stApp {background: #FFF8E7;}
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra - UNLIMITED")
st.caption("Photo + Voice - Telugu lo")

# --- KEYS ROTATION ---
try:
    KEYS = st.secrets["GROQ_KEYS"] # 2-3 keys pettu secrets lo
except:
    KEYS = [st.secrets["GROQ_API_KEY"]]

def get_client():
    return Groq(api_key=random.choice(KEYS))

def compress(b):
    img = Image.open(b)
    img.thumbnail((512,512))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60)
    return base64.b64encode(buf.getvalue()).decode()

lang = st.selectbox("Bhasha", ["Telugu", "English", "Hindi"])

tab1, tab2 = st.tabs(["📸 Photo Doctor", "🎙️ Voice + Photo MAGIC"])

with tab1:
    photo = st.file_uploader("Panta photo pettandi", type=["jpg","jpeg","png"], key="p1")
    if photo:
        st.image(photo, width=300)
        if st.button("Rogam Chudali 🔍", key="b1"):
            for _ in range(len(KEYS)):
                try:
                    client = get_client()
                    b64 = compress(photo)
                    with st.spinner(f"{lang} lo chustunna..."):
                        res = client.chat.completions.create(
                            model="qwen/qwen3.8-27b",
                            messages=[{"role":"user","content":[
                                {"type":"text","text":f"You are farm doctor. Answer ONLY in {lang}. Disease, Cause, Mandu, Prevention simple."},
                                {"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}]
                        )
                    st.success(res.choices[0].message.content)
                    st.balloons()
                    break
                except Exception as e:
                    if "RateLimit" in str(e) or "429" in str(e):
                        continue
                    else:
                        st.error(str(e))
                        break
            else:
                st.warning("⏳ Anni servers busy - 1 min aagi try cheyandi")

with tab2:
    st.write("Photo petti mic lo adagandi!")
    p2 = st.file_uploader("Photo", type=["jpg","jpeg","png"], key="p2")
    audio = st.audio_input("Mic nokki adagandi", key="a2")
    q = ""
    if audio:
        try:
            c = get_client()
            tr = c.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3")
            q = tr.text
            st.info(f"Meerannadi: {q}")
        except:
            pass
    q_text = st.text_input("Leda type cheyandi", value=q)
    if st.button("🔥 Magic Answer", key="b2"):
        if p2 and q_text:
            for _ in range(len(KEYS)):
                try:
                    c = get_client()
                    b64 = compress(p2)
                    with st.spinner("Magic..."):
                        res = c.chat.completions.create(model="qwen/qwen3.8-27b", messages=[{"role":"user","content":[{"type":"text","text":f"Q:{q_text} Answer in {lang} simple."},{"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}]}])
                    st.success(res.choices[0].message.content)
                    break
                except:
                    continue
        else:
            st.warning("Photo + Question pettandi")

st.divider()
st.markdown("**Made by Manish for Bharat Farmers 🇮🇳** | Streamlit Version - Always Free")
