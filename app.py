import streamlit as st
from google import genai

st.title("My Gemini App")

client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

prompt = st.text_input("Em adagali?")

if st.button("Ask Gemini"):
    with st.spinner("Thinking..."):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        st.write(response.text)
