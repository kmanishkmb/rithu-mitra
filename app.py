import streamlit as st
from groq import Groq

st.title("Rithu Mitra - Finally Working!")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

q = st.text_input("Em adagali? Nenu ready!")

if st.button("Adugu"):
    if q:
        with st.spinner("Alocistunna..."):
            try:
                chat = client.chat.completions.create(
                    model="openai/gpt-oss-20b", # IDHI KOTHA MODEL
                    messages=[
                        {"role": "user", "content": q}
                    ]
                )
                st.success(chat.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Question type chey")
