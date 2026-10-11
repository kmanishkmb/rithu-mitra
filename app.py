import streamlit as st
import requests

st.title("Rithu Mitra - Finally Working!")

API_KEY = st.secrets["GOOGLE_API_KEY"].strip()

q = st.text_input("Em adagali?")

if st.button("Adugu"):
    if q:
        with st.spinner("Alocistunna..."):
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

            headers = {
                "x-goog-api-key": API_KEY,
                "Content-Type": "application/json"
            }

            data = {
                "contents": [{"parts": [{"text": q}]}]
            }

            r = requests.post(url, headers=headers, json=data)
            res = r.json()

            if "candidates" in res:
                st.success(res["candidates"][0]["content"]["parts"][0]["text"])
            else:
                st.error(f"Error: {res}")
    else:
        st.warning("Question type chey")
