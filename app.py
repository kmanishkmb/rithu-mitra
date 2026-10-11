import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Rithu Mitra PRO", page_icon="🌾")
st.title("🌾 Rithu Mitra PRO - Voice + Photo Doctor")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

lang = st.selectbox("Bhasha / Language:", ["Telugu", "English", "Hindi", "Hinglish (Telugu + English)"])

tab1, tab2 = st.tabs(["🎙️ Voice / Text Prashna", "📸 Photo tho Rogam Check"])

# TAB 1
with tab1:
    audio = st.audio_input("Voice tho adagandi...")
    transcribed = ""
    if audio:
        with st.spinner("Text ga marchutunna..."):
            try:
                tr = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3")
                transcribed = tr.text
                st.info(f"Meerannadi: {transcribed}")
            except Exception as e:
                st.error(f"{e}")

    q = st.text_input("Prashna:", value=transcribed, key="q1", placeholder="Ex: Wari ki ye eruvulu?")

    if st.button("Answer Kavali 🌾", key="b1"):
        if q:
            with st.spinner(f"{lang} lo..."):
                try:
                    sys = f"You are Rithu Mitra farming expert. ALWAYS reply in {lang}. Simple words."
                    chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content":sys},{"role":"user","content":q}])
                    st.success(chat.choices[0].message.content)
                except Exception as e:
                    st.error(f"{e}")

# TAB 2 - FIXED
with tab2:
    st.subheader("Panta photo upload cheyandi")
    photo = st.file_uploader("Aaku / Panta photo", type=["jpg","jpeg","png"], key="photo")

    if photo:
        st.image(photo, caption="Me Panta Photo", width=300)
        if st.button("Rogam Enti Check Chey 🔍", key="photo_btn"):
            with st.spinner("Doctor chustunnadu..."):
                try:
                    b64 = base64.b64encode(photo.getvalue()).decode('utf-8')
                    sys = f"You are expert crop disease doctor. ALWAYS answer in {lang}. Tell: Disease, Cause, Solution, Prevention in simple {lang}."
                    chat = client.chat.completions.create(
                        model="qwen/qwen3.6-27b",
                        messages=[
                            {"role": "system", "content": sys},
                            {"role": "user", "content": [
                                {"type": "text", "text": f"Ee panta ki em aindi? Rogam cheppu in {lang}."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ]
                    )
                    st.success(chat.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")
