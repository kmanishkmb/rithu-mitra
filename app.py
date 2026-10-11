import streamlit as st
from groq import Groq

st.title("Rithu Mitra - Finally Working!")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

q = st.text_input("Em adagali?")

if st.button("Adugu"):
    if q:
        with st.spinner("Alocistunna..."):
            try:
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": q}]
                )
                st.success(chat.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
