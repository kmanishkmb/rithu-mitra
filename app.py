import streamlit as st
from groq import Groq

st.set_page_config(page_title="Rithu Mitra Voice", page_icon="🎙️")
st.title("🌾 Rithu Mitra - VOICE 🎙️")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

lang = st.selectbox("Bhasha / Language:", ["Telugu", "English", "Hindi", "Hinglish (Telugu + English)"])

st.divider()

# --- VOICE INPUT ---
st.subheader("🎙️ Voice tho Adagandi")
audio = st.audio_input("Mic nokki matladandi...")

transcribed_text = ""
if audio:
    with st.spinner("Vinipistunna... Text ga marchutunna..."):
        try:
            # Groq Whisper tho voice ni text ga marchadam
            transcription = client.audio.transcriptions.create(
                file=(audio.name, audio.getvalue()),
                model="whisper-large-v3",
                language="te" if lang=="Telugu" else "en" # Auto detect better
            )
            transcribed_text = transcription.text
            st.info(f"Meerannadi: **{transcribed_text}**")
        except Exception as e:
            st.error(f"Voice Error: {e}")

# --- TEXT INPUT ALSO ---
q_text = st.text_input("Leda ikkada type cheyandi:", value=transcribed_text, placeholder="Ex: Wari ki ye eruvulu?")

if st.button(f"Samadhanam Kavali - {lang} lo 🌾"):
    final_q = q_text or transcribed_text
    if final_q:
        with st.spinner(f"{lang} lo cheptunna..."):
            try:
                system_prompt = f"You are Rithu Mitra, farming expert. ALWAYS answer in {lang}. Simple words for farmers. If Hinglish, use Telugu in English letters."

                chat = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": final_q}
                    ]
                )
                st.success(chat.choices[0].message.content)
                # Optional: Text to speech kuda cheyochu tarwata
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Mundu matladandi leda type cheyandi!")

st.divider()
st.markdown("Made with ❤️ by Manish | Voice Powered by Groq")
