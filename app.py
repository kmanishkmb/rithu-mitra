import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra UNLIMITED", page_icon="🌾")

st.markdown("<h1 style='text-align:center;'>🌾 Rithu Mitra</h1><p style='text-align:center;'>Telugu + Photo = Magic</p>", unsafe_allow_html=True)

try:
    KEYS = st.secrets["GROQ_KEYS"]
except:
    KEYS = [st.secrets.get("GROQ_API_KEY")]

def client(): return Groq(api_key=random.choice(KEYS))
def to_b64(file):
    img = Image.open(file)
    img.thumbnail((512,512))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60)
    return base64.b64encode(buf.getvalue()).decode()

lang = st.selectbox("Bhasha", ["Telugu","English","Hindi"])

# --- DIFFERENT TABS WITH DIFFERENT KEYS ---
t1, t2 = st.tabs(["📸 ONLY PHOTO", "🎙️ PHOTO + VOICE"])

with t1:
    st.subheader("Photo pettandi - Nene cheptha")
    f1 = st.file_uploader("Photo upload", type=["jpg","png","jpeg"], key="only_photo")
    if f1:
        st.image(f1, width=250)
        if st.button("🔍 Rogam Enti?", key="btn_photo_only"):
            try:
                b64 = to_b64(f1)
                c = client()
                ans = c.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[{"role":"user","content":[
                        {"type":"text","text":f"Identify crop disease from photo. Answer in {lang}. Give Disease, Reason, Mandu."},
                        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                    ]}]
                )
                st.success(ans.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

with t2:
    st.subheader("Photo + Voice Magic")
    f2 = st.file_uploader("Photo upload", type=["jpg","png","jpeg"], key="photo_voice")
    aud = st.audio_input("Meeru adagandi", key="voice_input")
    q = ""
    if aud:
        try:
            c2 = client()
            tr = c2.audio.transcriptions.create(file=(aud.name, aud.getvalue()), model="whisper-large-v3")
            q = tr.text
            st.info(f"Vinnadi: {q}")
        except Exception as e:
            st.warning("Voice vinadam lo error, type cheyandi")

    q_input = st.text_input("Question", value=q, key="q_text_voice")

    if st.button("✨ Magic Answer", key="btn_voice_magic"):
        if f2 and q_input:
            try:
                b64 = to_b64(f2)
                c = client()
                ans = c.chat.completions.create(
                    model="llama-3.2-90b-vision-preview",
                    messages=[{"role":"user","content":[
                        {"type":"text","text":f"Farmer asks: {q_input}. Photo chusi {lang} lo samadhanam cheppu."},
                        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
                    ]}]
                )
                st.success(ans.choices[0].message.content)
                st.balloons()
            except Exception as e:
                st.error(str(e))
        else:
            st.warning("Photo + Question rendu kavali")
