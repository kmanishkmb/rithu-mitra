import streamlit as st
from groq import Groq

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")
st.title("🌾 Rithu Mitra - రైతు మిత్ర")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Language Selector
lang = st.selectbox("Bhasha / Language Select Cheyandi:",
    ["Telugu", "English", "Hindi", "Tamil", "Kannada", "Hinglish (Telugu + English)"]
)

q = st.text_input("Prashna / Question:", placeholder="Ex: Wari ki ye eruvulu veyali? / What fertilizer for paddy?")

if st.button(f"Adugu - {lang} lo 🌾"):
    if q:
        with st.spinner(f"{lang} lo alocistunna..."):
            try:
                # Dynamic prompt based on language
                system_prompt = f"You are Rithu Mitra, a friendly farming expert. ALWAYS answer in {lang}. Use simple, easy words for farmers. If language is Hinglish, use Telugu words written in English letters mixed with English. Be helpful about crops, fertilizers, pests."

                chat = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": q}
                    ]
                )
                st.success(chat.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Prashna type cheyandi!")

st.divider()
st.markdown("Made with ❤️ by Manish for farmers")
