import streamlit as st
from groq import Groq
import base64

st.set_page_config(page_title="Rithu Mitra PRO", page_icon="🌾")
st.title("🌾 Rithu Mitra PRO - Photo Doctor")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
lang = st.selectbox("Bhasha:", ["Telugu", "English", "Hindi", "Hinglish (Telugu + English)"])

tab1, tab2 = st.tabs(["🎙️ Voice / Text", "📸 Photo Doctor"])

with tab1:
    audio = st.audio_input("Voice tho adagandi...")
    transcribed = ""
    if audio:
        tr = client.audio.transcriptions.create(file=(audio.name, audio.getvalue()), model="whisper-large-v3")
        transcribed = tr.text
        st.info(f"Meerannadi: {transcribed}")

    q = st.text_input("Prashna:", value=transcribed, key="q1")
    if st.button("Answer Kavali 🌾", key="b1"):
        if q:
            chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=[{"role":"system","content": f"ALWAYS answer in {lang}."},{"role":"user","content": q}])
            st.success(chat.choices[0].message.content)

with tab2:
    st.subheader("📸 Photo Upload - Groq Vision")
    photo = st.file_uploader("Panta photo", type=["jpg","jpeg","png"], key="photo2")

    if photo:
        st.image(photo, caption="Me Panta Photo", width=300)
        if st.button("Rogam Enti Check Chey 🔍", key="pb2"):
            with st.spinner(f"{lang} lo Doctor chustunnadu... (Groq qwen3.8)"):
                try:
                    b64 = base64.b64encode(photo.getvalue()).decode('utf-8')

                    # NEW MODEL - qwen3.8-27b
                    chat = client.chat.completions.create(
                        model="qwen/qwen3.8-27b",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": f"You are crop disease doctor. Look at this crop image. Explain in {lang}: Disease name, Cause, Solution/Mandu, Prevention. Simple words for farmers."},
                                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                                ]
                            }
                        ]
                    )
                    st.success(chat.choices[0].message.content)

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Tip: Free tier lo okasari fail ayite 1 min tarwata malli try cheyandi - rate limit valla kuda 404 vastadi.")
