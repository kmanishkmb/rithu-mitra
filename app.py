import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Rithu Mitra PRO MAX", page_icon="🚀")
st.title("🚀 Rithu Mitra PRO MAX")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
lang = st.selectbox("Bhasha:", ["Telugu", "English", "Hindi", "Hinglish"])

tab1, tab2, tab3 = st.tabs(["🎙️ Voice Prashna", "📸 Photo Doctor", "🔥 Voice + Photo = MAGIC"])

# TAB 1 & 2 - same as before (copy chesuko)

with tab1:
    audio = st.audio_input("Voice tho adagandi...", key="a1")
    transcribed = ""
    if audio:
        tr = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3")
        transcribed = tr.text
        st.info(f"Meerannadi: {transcribed}")
    q = st.text_input("Prashna:", value=transcribed, key="q1")
    if st.button("Answer Kavali 🌾", key="b1"):
        if q:
            chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content": f"ALWAYS in {lang}"},{"role":"user","content": q}])
            st.success(chat.choices[0].message.content)

with tab2:
    photo = st.file_uploader("Panta photo", type=["jpg","jpeg","png"], key="p2")
    if photo:
        st.image(photo, width=300)
        if st.button("Rogam Check 🔍", key="b2"):
            b64 = base64.b64encode(photo.getvalue()).decode('utf-8')
            chat = client.chat.completions.create(model="qwen/qwen3.8-27b", messages=[{"role":"user","content": [{"type":"text","text": f"Disease doctor. Answer in {lang}: Disease, Cause, Mandu, Prevention."},{"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}]}])
            st.success(chat.choices[0].message.content)

# TAB 3 - NEW MAGIC
with tab3:
    st.subheader("Photo + Voice Kalipi Adagandi!")
    st.write("Photo petti, mic lo adigite - AI rendu kalipi samadhanam istadi!")

    c1, c2 = st.columns(2)
    with c1:
        magic_photo = st.file_uploader("1. Photo pettandi", type=["jpg","jpeg","png"], key="magic_p")
        if magic_photo:
            st.image(magic_photo, width=250)

    with c2:
        magic_audio = st.audio_input("2. Photo gurinchi adagandi", key="magic_a")
        magic_trans = ""
        if magic_audio:
            tr = client.audio.transcriptions.create(file=(magic_audio.name, magic_audio.getvalue()), model="whisper-large-v3")
            magic_trans = tr.text
            st.success(f"Question: {magic_trans}")

    magic_q = st.text_input("Leda type cheyandi:", value=magic_trans, placeholder="Ex: Ee mokka ki em mandu veyali?", key="magic_q")

    if st.button("🔥 Magic Answer Kavali!", key="magic_b"):
        if magic_photo and magic_q:
            with st.spinner(f"{lang} lo Magic chestunna..."):
                b64 = base64.b64encode(magic_photo.getvalue()).decode('utf-8')
                full_prompt = f"Raitu prashna: '{magic_q}'. Ee photo chusi {lang} lo simple ga cheppu. Disease, Mandu, Jagrattalu."

                chat = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=[{"role":"user","content": [{"type":"text","text": full_prompt},{"type":"image_url","image_url":{"url": f"data:image/jpeg;base64,{b64}"}}]}]
                )
                st.balloons()
                st.success(chat.choices[0].message.content)
        else:
            st.warning("Photo + Voice / Text rendu pettandi Manish!")

st.divider()
st.markdown("**Rithu Mitra PRO MAX by Manish - India's First Voice + Vision Farmer AI 🚀**")
