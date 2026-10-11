import streamlit as st
from google import genai

st.title("My Gemini App")
st.write("App is running!")

try:
    client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    prompt = st.text_input("Em adagali?")
    
    if st.button("Ask Gemini"):
        if prompt:
            with st.spinner("Thinking..."):
                # AQ key ki best model idi
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success(response.text)
        else:
            st.warning("Mundhu emaina type chey!")
            
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Secrets lo API key correct ga unda chudu")
