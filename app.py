import streamlit as st
from google import genai
from PIL import Image

MY_KEY = st.secrets["AQ.Ab8RN6Lx_5CAnvjVmps3-Wb2CrAivgNXloweTrLJcO2wz_LefQ"]
client = genai.Client(api_key=MY_KEY)

st.set_page_config(page_title="Rithu Mitra 2.0", page_icon="🌾")
st.title("🌾 Rithu Mitra 2.0")
st.write("Mirapa / Tomato / Vankaya - Edaina panta photo pettandi!")

uploaded_file = st.file_uploader("Photo Upload chey", type=["jpg", "jpeg", "png"])
question = st.text_input("Adagandi (Ex: Ee aaku enduku mudathapadindi?)")

if st.button("🔍 Pariksha Chey"):
	if not uploaded_file and not question:
		st.warning("Dayachesi photo or question ivvandi")
	else:
		with st.spinner("Rithu Mitra pariselisthunnadu..."):
			telugu_prompt = f"Nuvvu Srikakulam ki chendina telugu rythu sahayakudivi. User prashna: {question}. Dayachesi 100% Telugu lo cheppu."
			if uploaded_file:
				img = Image.open(uploaded_file)
				st.image(img, caption="Mee Panta", use_container_width=True)
				response = client.models.generate_content(
					model="gemini-3.8-flash", contents=[telugu_prompt, img]
				)
			else:
				response = client.models.generate_content(
					model="gemini-3.8-flash", contents=telugu_prompt
				)
			st.success("Pariksha Poorthi Ayindi!")
			st.markdown(response.text)

st.sidebar.info("Made with ❤️ by Manish for AP Farmers")
