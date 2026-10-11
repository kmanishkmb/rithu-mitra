import streamlit as st
import requests
import json

st.title("Rithu Mitra - Finally Working!")

API_KEY = st.secrets["GOOGLE_API_KEY"]

q = st.text_input("Em adagali? Nenu ready!")

if st.button("Adugu"):
    if q:
        with st.spinner("Alocistunna..."):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

            data = {
                "contents": [{"parts": [{"text": q}]}]
            }

            try:
                response = requests.post(url, json=data, timeout=30)
                result = response.json()

                if "candidates" in result:
                    answer = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.success(answer)
                else:
                    st.error(f"API Error: {result}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Question type chey")
