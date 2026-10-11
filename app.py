import streamlit as st
from google import genai

st.title("Rithu Mitra")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

q = st.text_input("Em adagali?")
if st.button("Adugu"):
    if q:
        res = client.models.generate_content(model="gemini-2.0-flash", contents=q)
        st.write(res.text)
