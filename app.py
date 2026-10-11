import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")

# --- BLUE THEME ---
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
[data-testid="stHeader"] { background-color: #E3F2FD; }
h1, h2, h3 { color: #0D47A1!important; }
.stTabs [data-baseweb="tab"] { background-color: white; border-radius: 10px; }
.stButton>button { background-color: #1976D2; color: white; border-radius: 10px; width: 100%; }
.stButton>button:hover { background-color: #0D47A1; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra")
st.markdown("<p style='color:#1565C0;'>💙 Blue Theme | Telugu lo Rithu Sahayam</p>", unsafe_allow_html=True)

try:
    KEYS = st.secrets["GROQ_KEYS"]
except:
    KEYS = [st.secrets.get("GROQ_API_KEY")]

def client(): return Groq(api_key=random.choice(KEYS))
def to_b64(file):
    img = Image.open(file)
    img.thumbnail((600,600))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode()

lang = st.selectbox("Bhasha", ["Telugu","English","Hindi"])

t1, t2 = st.tabs(["📸 Photo Doctor", "🎙️ Voice + Photo"])

with t1:
    f1 = st.file_uploader("Panta photo", type=["jpg","png","jpeg"], key="p1")
    if f1:
        st.image(f1, width=300)
        if st.button("Rogam Enti? 🔍", key="b1"):
            with st.spinner("Chustunna..."):
                try:
                    c = client()
                    b64 = to_b64(f1)
                    res = c.chat.completions.create(
                        model="meta-llama/llama-4-maverick-17b-128e-instruct",
                        messages=[{"role":"user","content":[
                            {"type":"text","text":f"Farm photo analyse chey. {lang} lo cheppu. Disease, Karanam, Mandu."},
                            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                        ]}]
                    )
                    st.success(res.choices[0].message.content)
                except Exception as e:
                    st.error(str(e))

with t2:
    f2 = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="p2")
    aud = st.audio_input("Voice adagandi", key="a1")
    q_text = ""
    if aud:
        try:
            c = client()
            tr = c.audio.transcriptions.create(file=(aud.name, aud.getvalue()), model="whisper-large-v3")
            q_text = tr.text
            st.info(f"Meerannadi: {q_text}")
        except:
            pass
    q = st.text_input("Question", value=q_text, key="q1")
    if st.button("Magic Answer ✨", key="b2"):
        if f2 and q:
            with st.spinner("Magic..."):
                try:
                    c = client()
                    b64 = to_b64(f2)
                    res = c.chat.completions.create(
                        model="meta-llama/llama-4-maverick-17b-128e-instruct",
                        messages=[{"role":"user","content":[
                            {"type":"text","text":f"Q: {q}. Photo chusi {lang} lo cheppu."},
                            {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                        ]}]
                    )
                    st.success(res.choices[0].message.content)
                    st.balloons()
                except Exception as e:
                    st.error(str(e))
        else:
            st.warning("Photo + Question pettandi")
