import streamlit as st
from groq import Groq
import base64
from PIL import Image
import io

st.set_page_config(page_title="Rithu Mitra PRO MAX", page_icon="🚀")
st.title("🚀 Rithu Mitra PRO MAX")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
lang = st.selectbox("Bhasha:", ["Telugu", "English", "Hindi", "Hinglish"])

def compress_image(uploaded_file):
    # Photo ni 512x512 ki compress chestunna - token save avuthadi
    img = Image.open(uploaded_file)
    img.thumbnail((512, 512))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

tab1, tab2, tab3 = st.tabs(["🎙️ Voice", "📸 Photo", "🔥 Magic"])

with tab1:
    audio = st.audio_input("Voice tho adagandi...", key="a1")
    transcribed = ""
    if audio:
        try:
            tr = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3")
            transcribed = tr.text
            st.info(f"Meerannadi: {transcribed}")
        except Exception as e:
            if "RateLimit" in str(e):
                st.warning("⏳ Konchem aagi 1 min tarwata try cheyandi - Groq limit ayindi")
            else:
                st.error(e)

    q = st.text_input("Prashna:", value=transcribed, key="q1")
    if st.button("Answer Kavali 🌾", key="b1"):
        if q:
            try:
                chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content": f"ALWAYS in {lang}"},{"role":"user","content": q}])
                st.success(chat.choices[0].message.content)
            except Exception as e:
                if "RateLimit" in str(type(e)) or "429" in str(e):
                    st.warning(f"⏳ Groq free limit ayindi Manish. 1-2 nimishalu aagi malli nokkandi. {lang} lo.")
                else:
                    st.error(e)

with tab2:
    photo = st.file_uploader("Panta photo", type=["jpg","jpeg","png"], key="p2")
    if photo:
        st.image(photo, width=300)
        if st.button("Rogam Check 🔍", key="b2"):
            with st.spinner(f"{lang} lo chustunna..."):
                try:
                    b64 = compress_image(photo)
                    chat = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[{"role":"user","content": [{"type":"text","text": f"Disease doctor. Answer in {lang}: Disease, Cause, Mandu, Prevention."},{"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}]}]
                    )
                    st.success(chat.choices[0].message.content)
                except Exception as e:
                    if "RateLimit" in str(type(e).__name__) or "rate_limit" in str(e).lower() or "429" in str(e):
                        st.error("🚨 Groq Free Limit Ayindi!")
                        st.warning("""
                        **Fix:**
                        1. 2 nimishalu aagi malli try cheyandi
                        2. Leda inkoka Groq API key create chesi secrets lo 2nd key pettandi
                        3. Roju ki 15 photos mathrame free - repu malli vastadi
                        """)
                    else:
                        st.error(f"Error: {e}")

with tab3:
    st.subheader("Voice + Photo Magic")
    magic_photo = st.file_uploader("1. Photo", type=["jpg","jpeg","png"], key="magic_p")
    magic_audio = st.audio_input("2. Voice Q", key="magic_a")
    magic_trans = ""
    if magic_audio:
        tr = client.audio.transcriptions.create(file=(magic_audio.name, magic_audio.getvalue()), model="whisper-large-v3")
        magic_trans = tr.text
        st.success(f"Q: {magic_trans}")
    magic_q = st.text_input("Question:", value=magic_trans, key="magic_q")
    if st.button("🔥 Magic Answer!", key="magic_b"):
        if magic_photo and magic_q:
            try:
                b64 = compress_image(magic_photo)
                chat = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=[{"role":"user","content": [{"type":"text","text": f"Q: {magic_q}. Answer in {lang}. Simple."},{"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}]}])
                st.balloons()
                st.success(chat.choices[0].message.content)
            except Exception as e:
                st.warning("⏳ Limit ayindi - 1 min aagi try cheyandi Manish!")

st.caption("Tip: RateLimit vasthe 2 min aagandi - auto fix avuthadi")
