import streamlit as st
import io
from gtts import gTTS
from google import genai
from PIL import Image
client = genai.Client(api_key=st.secrets['ARSALAN'])
st.set_page_config(
    page_title="Arsalan's AI",
    page_icon="✨"
)
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #090d16 !important;
        background-image: radial-gradient(circle at 50% 50%, #0d1527 0%, #060910 100%) !important;
    }
    [data-testid="stBottom"] {
        background-color: transparent !important;
        background-image: none !important;
    }
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
        background-image: none !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebarUserContent"] {
        background-color: #05080e !important;
        border-right: 2px solid #00f0ff !important;
        box-shadow: 4px 0 15px rgba(0, 240, 255, 0.15) !important;
    }
    .stLinkButton>a {
        background-color: #111724 !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        display: block !important;
        text-align: center !important;
        text-decoration: none !important;
        box-shadow: 0 0 8px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stLinkButton>a:hover {
        background-color: #00f0ff !important;
        color: #05080e !important;
        box-shadow: 0 0 15px #00f0ff !important;
    }
    .stDownloadButton>button {
        background-color: #111a1a !important;
        color: #39ff14 !important;
        border: 1px solid #39ff14 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        display: block !important;
        box-shadow: 0 0 8px rgba(57, 255, 20, 0.1) !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stDownloadButton>button:hover {
        background-color: #39ff14 !important;
        color: #05080e !important;
        box-shadow: 0 0 15px #39ff14 !important;
    }
    .stFileUploader, [data-testid="stFileUploaderDropzone"], div[data-testid="stFileUploadDropzone"] {
        background-color: #111724 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 12px !important;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.1) !important;
        transition: all 0.3s ease-in-out !important;
    }
    .stFileUploader:hover, [data-testid="stFileUploaderDropzone"]:hover, div[data-testid="stFileUploadDropzone"]:hover {
        border-color: #39ff14 !important;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.3) !important;
    }
    [data-testid="stFileUploaderDropzone"] button, .stFileUploader button {
        background-color: #1a233a !important;
        color: #00f0ff !important;
        border: 1px solid #00f0ff !important;
        border-radius: 6px !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 15px #00f0ff !important;
    }
    [data-testid="stChatInputSubmitButton"] {
        background-color: #00f0ff !important;
        color:rgb(255,255,255) !important;
        font-weight:bold !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover {
        box-shadow: 0 0 12px #00f0ff !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stChatInputSubmitButton"]:disabled {
        background-color: #4A4A4A !important;
    }
    [data-testid="stChatInputSubmitButton"]:disabled * {
        color: #8E8E8E !important;
        fill: #8E8E8E !important;
        stroke: #8E8E8E !important;
    }
    [data-testid="stChatInputSubmitButton"]:not(:disabled) {
        background-color: #DE5D83 !important;
    }
    .stButton>button {
        background-color: #1a1115 !important;
        color: #ff0055 !important;
        border: 1px solid #ff0055 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        display: block !important;
        box-shadow: 0 0 8px rgba(255, 0, 85, 0.1) !important;
        transition: all 0.25s ease-in-out !important;
    }
    .stButton>button:hover {
        background-color: #ff0055 !important;
        color: #05080e !important;
        box-shadow: 0 0 15px #ff0055 !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("Arsalan's AI v1.0")
st.write("Made by Arsalan Ali Khan. Teenager genius.")
if 'memory' not in st.session_state:
    st.session_state.memory=[]
chat_block = st.container()
with chat_block:
    for chat in st.session_state.memory:
        if chat['role']=="User":
            with st.chat_message('user'):
                st.write(f"**User:** {chat['text']}")
        elif chat['role'] == "AI":
            with st.chat_message('assistant'):
                st.write(f"**AI:** {chat['text']}")
            if "audio" in chat:
                st.audio(chat['audio'], format='audio/mp3')
    st.write("___________________________________________")
upl=None
h = st.sidebar.title("Arsalan's AI v1.0")
if st.checkbox("Did you want to Upload File?",value=False):
    upl=st.file_uploader("Upload File!",type=["jpg","png"])
user = st.chat_input("Ask Arsalan's AI:")
langs = st.sidebar.selectbox("Voice Language selector:", ["English", "Urdu"])
h2 = st.sidebar.header("Additional utilities")
cal = st.sidebar.link_button("Calculator", "https://alikhan30795.github.io/Calculator-JS/")
psc = st.sidebar.link_button("Password Strength checker", "https://alikhan30795.github.io/psc/")
tg = st.sidebar.link_button("Tables Generator", "https://alikhan30795.github.io/Tables/")
gg = st.sidebar.link_button("Guessing game", "https://alikhan30795.github.io/Guess/")
chat_text = ""
for chat in st.session_state.memory:
    chat_text += f"{chat['role']}: {chat['text']}\n"
if chat_text: 
    st.sidebar.header("Download Chat!")
    st.sidebar.download_button(
        label="Download Chat History 📄",
        data=chat_text,
        file_name="arsalan_ai_chat.txt",
        mime="text/plain",
        on_click="ignore"
    )
st.sidebar.header("Clear chat")
if st.sidebar.button("Clear Chat 🗑️"):
    st.session_state.memory = []
    st.rerun()
st.sidebar.header("AI Results in Coding")
st.sidebar.link_button("Website development using this model","https://arsalan-store-e9ux4x9n2-alikhan30795.vercel.app/")
st.sidebar.header("ℹ️ Developer Info")
st.sidebar.write("Created by Arsalan Ali Khan — 9th Class Genius 😎")
st.sidebar.write("---")
if user:
    inp=[]
    if upl is not None:
        img=Image.open(upl)
        inp.append(img)
        inp.append(f"Analyze The Image based on User's Request{user}")
    else:
        inp.append(user)
    user_lower = user.lower()
    id = [
        "who are you", "made you", "creator", "owner", 
        "tum kon ho", "kisne banaya", "kis ne banaya", 
        "kis ne bnaya", "tumhe kisne", "tumhe kis ne"
    ]
    qid = ["quiz", "test", "mcq"]
    with chat_block:
        with st.chat_message('user'):
            st.write(f"**User:** {user}")  
    if any(w in user_lower for w in id):
        reply = "Hello Buddy, Iam Arsalan's AI.A simple AI Programmed By genius Arsalan. "
        st.session_state.memory.append({"role": "User", "text": user})
        st.session_state.memory.append({"role": "AI", "text": reply})
        st.rerun()       
    elif any(q in user_lower for q in qid):
        with chat_block:
            with st.spinner("Generating Quiz !"):
                try:
                    quiz = f"Generate multiple choice quiz based on {user}."
                    qu_res = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=quiz
                        )
                    st.session_state.memory.append({"role": "User", "text": user})
                    st.session_state.memory.append({"role": "AI", "text": qu_res.text})                
                    st.rerun()
                except Exception as e:
                    st.error(f"Quiz error, {e}")
    else:
        with chat_block:
            with st.spinner("AI is thinking !"):
                try:
                    context = "system: You are Arsalan's assistant.A Teenager Tech genius."
                    for c in st.session_state.memory:
                        context += f"{c['role']} : {c['text']}\n"
                    context += f"User:{user}"
                    inp.append(context)
                    response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=inp
                        )   
                    sellang = "en"
                    if langs == "Urdu":
                        sellang = "ur"     
                    tts = gTTS(text=response.text[:200], lang=sellang)
                    pocket = io.BytesIO()
                    tts.write_to_fp(pocket)
                    st.session_state.memory.append({"role": "User", "text": user})
                    st.session_state.memory.append({"role": "AI", "text": response.text, "audio": pocket.getvalue()})
                    with st.chat_message('assistant'):
                        st.write(f"**AI:** {response.text}")
                except Exception as e:
                    st.error(f"An Error Occured! Please try again! {e}")
