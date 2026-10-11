import streamlit as st
from groq import Groq
import base64, random, io
from PIL import Image

st.set_page_config(page_title="Rithu Mitra", page_icon="🌾")

# BLUE THEME - FULL FORCE
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #E3F2FD 0%, #90CAF9 100%)!important; }
[data-testid="stHeader"] { background: #E3F2FD!important; }
h1 { color: #0D47A1!important; text-align: center; }
div.stButton > button { background: #0D47A1!important; color: white!important; border-radius: 20px!important; height: 60px!important; font-size: 18px!important; width: 100%!important; }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Rithu Mitra 💙")
st.markdown("<center><b style='color:#0D47A1;'>GROQ POWERED - Blue Theme</b></center>", unsafe_allow_html=True)

# --- GROQ KEYS ---
try:
    KEYS = st.secrets["GROQ_KEYS"]
    st.toast(f"{len(KEYS)} Keys Loaded!")
except:
    KEYS = [st.secrets["GROQ_API_KEY"]]

def get_client():
    return Groq(api_key=random.choice(KEYS))

def to_b64(f):
    img = Image.open(f)
    img.thumbnail((500,500))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=60)
    return base64.b64encode(buf.getvalue()).decode()

# GROQ CURRENT VISION MODELS - AUTO TRY
MODELS_TO_TRY = [
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct"
]

def ask_vision(prompt, b64):
    for model_name in MODELS_TO_TRY:
        try:
            client = get_client()
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                    ]
                }],
                max_tokens=800,
                temperature=0.4
            )
            return resp.choices[0].message.content, model_name
        except Exception as e:
            last_err = str(e)
            continue
    return f"❌ Groq Error: {last_err}. Keys check chey console.groq.com lo", None

lang = st.selectbox("Bhasha", ["Telugu", "English"], key="lang")

t1, t2 = st.tabs(["📸 Photo", "🎙️ Voice + Photo"])

with t1:
    f = st.file_uploader("Panta photo pettu", type=["jpg","png","jpeg"], key="p1")
    if f:
        st.image(f, width=300)
        if st.button("Rogam Enti? 🔍", key="btn1", use_container_width=True):
            with st.spinner("Groq Scout chustondi..."):
                b64 = to_b64(f)
                ans, used_model = ask_vision(f"Crop disease identify chey. Answer in {lang}. Format: Rogam:, Karanam:, Mandu:, Nivarana:", b64)
                if used_model:
                    st.success(ans)
                    st.caption(f"✅ Model: {used_model}")
                    st.balloons()
                else:
                    st.error(ans)

with t2:
    f2 = st.file_uploader("Photo", type=["jpg","png","jpeg"], key="p2")
    q = st.text_input("Prashna rayi: mandhu enti?", key="q2")
    if st.button("Magic ✨", key="btn2", use_container_width=True):
        if f2 and q:
            with st.spinner("..."):
                b64 = to_b64(f2)
                ans, used_model = ask_vision(f"Farmer asks: {q}. Photo chusi {lang} lo cheppu.", b64)
                if used_model:
                    st.success(ans)
                else:
                    st.error(ans)
        else:
            st.warning("Photo + Question rendu pettu")

st.divider()
if st.button("🔍 Check My Groq Models"):
    try:
        c = get_client()
        models = c.models.list()
        vision_models = [m.id for m in models.data if "vision" in str(m.id).lower() or "scout" in m.id or "maverick" in m.id or "qwen" in m.id or "llama-4" in m.id]
        st.write("Nee account ki available vision models:")
        st.json(vision_models)
        st.write("Full list:")
        st.json([m.id for m in models.data][:20])
    except Exception as e:
        st.error(f"List error: {e}")
