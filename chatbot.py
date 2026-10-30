import streamlit as st
import io
from gtts import gTTS
from google import genai
from PIL import Image

st.set_page_config(
    page_title="Arsalan's AI",
    page_icon="images.jpg"
)

client = genai.Client(api_key=st.secrets["ARSALAN"])
st.logo("images.jpg")

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
    st.session_state.memory = []

chat_block = st.container()
with chat_block:
    for chat in st.session_state.memory:
        if chat['role'] == "User":
            with st.chat_message('user'):
                st.write(f"**User:** {chat['text']}")
        elif chat['role'] == "AI":
            with st.chat_message('assistant'):
                st.write(f"**AI:** {chat['text']}")
            if "audio" in chat:
                st.audio(chat['audio'], format='audio/mp3')
    st.write("___________________________________________")

upl = None
h = st.sidebar.title("Arsalan's AI v1.0")

if st.checkbox("Did you want to Upload File?", value=False):
    upl = st.file_uploader("Upload File!", type=["jpg", "png"])

prompt_input = st.chat_input("Ask Arsalan's AI or click mic to speak!", accept_audio=True)

langs = st.sidebar.selectbox("Voice Language selector:", ["English", "Urdu"])
st.sidebar.write("---")
h2 = st.sidebar.header("Additional utilities")
cal = st.sidebar.link_button("Calculator", "https://github.io")
psc = st.sidebar.link_button("Password Strength checker", "https://github.io")
tg = st.sidebar.link_button("Tables Generator", "https://github.io")
gg = st.sidebar.link_button("Guessing game", "https://github.io")
st.sidebar.write("---")
st.sidebar.header("Clear chat")

if st.sidebar.button("Clear Chat 🗑️"):
    st.session_state.memory = []
    st.rerun()

st.sidebar.write("---")
st.sidebar.header("AI Results in Coding")
st.sidebar.link_button("Website development using this model", "https://vercel.app")
st.sidebar.write("---")
st.sidebar.header("ℹ️ Developer Info")
st.sidebar.write("Created by Arsalan Ali Khan — 9th Class Genius 😎")
st.sidebar.write("---")

if prompt_input:
    final_user_text = ""
    
    if prompt_input.audio:
        with st.spinner("Converting Voice to Text..."):
            try:
                audio_data = prompt_input.audio.getvalue()
                transcribe_prompt = "Transcribe this audio strictly into text. Do not add any extra explanation or greeting."
                audio_part = {"data": audio_data, "mime_type": "audio/wav"}
                
                stt_res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[audio_part, transcribe_prompt]
                )
                final_user_text = stt_res.text.strip()
            except Exception as e:
                st.error(f"Voice Recognition Error: {e}")
                final_user_text = "Audio Message"
    elif prompt_input.text:
        final_user_text = prompt_input.text

    if final_user_text:
        inp = []
        if upl is not None:
            img = Image.open(upl)
            inp.append(img)
            inp.append(f"Analyze The Image based on User's Request: {final_user_text}")
        else:
            inp.append(final_user_text)

        user_lower = final_user_text.lower()
        id = [
            "who are you", "made you", "creator", "owner", 
            "tum kon ho", "kisne banaya", "kis ne banaya", 
            "kis ne bnaya", "tumhe kisne", "tumhe kis ne"
        ]
        
        with chat_block:
            with st.chat_message('user'):
                st.write(f"**User:** {final_user_text}")  
        
        if any(w in user_lower for w in id):
            reply = "Hello Buddy, I am Arsalan's AI. A simple AI Programmed By genius Arsalan."
        else:
            with st.spinner("Arsalan's AI is thinking..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=inp
                    )
                    reply = response.text
                except Exception as e:
                    reply = f"Error: {e}"

        audio_fp = io.BytesIO()
        lang_code = "en" if langs == "English" else "ur"
        try:
            tts = gTTS(text=reply, lang=lang_code, slow=False)
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            audio_bytes = audio_fp.read()
        except Exception as e:
            audio_bytes = None

        st.session_state.memory.append({"role": "User", "text": final_user_text})
        
        ai_memory_data = {"role": "AI", "text": reply}
        if audio_bytes:
            ai_memory_data["audio"] = audio_bytes
            
        st.session_state.memory.append(ai_memory_data)
        st.rerun()
