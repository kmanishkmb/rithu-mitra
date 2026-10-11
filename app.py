import streamlit as st
import google.generativeai as genai

st.title("My Gemini App")
st.write("App is running!")

# API Key load
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = st.text_input("Em adagali?")
    
    if st.button("Ask Gemini"):
        if prompt:
            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)
                st.success(response.text)
        else:
            st.warning("Okati type chey Manish!")
            
except Exception as e:
    st.error(f"Error: {e}")
