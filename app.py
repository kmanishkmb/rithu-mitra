# TAB 2 - PHOTO DISEASE - FIXED MODEL
with tab2:
    st.subheader("Panta photo upload cheyandi")
    photo = st.file_uploader("Aaku / Panta photo", type=["jpg","jpeg","png"], key="photo")

    if photo:
        st.image(photo, caption="Me Panta Photo", width=300)
        if st.button("Rogam Enti Check Chey 🔍", key="photo_btn"):
            with st.spinner("Doctor chustunnadu... (Kotta AI tho)"):
                try:
                    import base64
                    b64 = base64.b64encode(photo.getvalue()).decode('utf-8')

                    sys = f"You are an expert crop disease doctor. ALWAYS answer in {lang}. Look at crop image and tell: 1. Disease name 2. Cause 3. Solution / Mandu 4. Prevention. Simple {lang}."

                    # NEW WORKING MODEL - QWEN 3.6 (Groq's new vision model)
                    chat = client.chat.completions.create(
                        model="qwen/qwen3.6-27b",
                        messages=[
                            {"role": "system", "content": sys},
                            {"role": "user", "content": [
                                {"type": "text", "text": f"Ee panta ki em aindi? Rogam cheppu in {lang}."},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                            ]}
                        ]
                    )
                    st.success(chat.choices[0].message.content)

                except Exception as e:
                    st.error(f"Error: {e}")
                    st.warning("Alternative: Groq lo Vision temporary down ayite, photo gurinchi text lo cheppandi - 'Wari aaku pasupu rangulo undi' ani - answer vastadi!")
