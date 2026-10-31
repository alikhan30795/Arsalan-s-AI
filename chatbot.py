
import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Arsalan's AI",
    page_icon="images.jpg",
    layout="wide"
)

MODEL = "gemini-3.5-flash-lite"

try:
    client = genai.Client(api_key=st.secrets["ARSALAN"])
except Exception as e:
    st.error(f"API Error: {e}")
    st.stop()

if "memory" not in st.session_state:
    st.session_state.memory = []

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #090d16 !important;
    background-image: radial-gradient(circle at 50% 50%, #0d1527 0%, #060910 100%) !important;
}
[data-testid="stSidebar"] {
    background-color: #05080e !important;
    border-right: 2px solid #00f0ff !important;
    box-shadow: 4px 0 15px rgba(0,240,255,0.15) !important;
}
h1, h2, h3 {
    color: #00f0ff !important;
    text-shadow: 0 0 10px rgba(0,240,255,0.4);
}
p, label {
    color: #d6e4ff !important;
}
.stButton > button {
    background-color: #1a1115 !important;
    color: #ff0055 !important;
    border: 1px solid #ff0055 !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    width: 100% !important;
    transition: 0.3s !important;
}
.stButton > button:hover {
    background-color: #ff0055 !important;
    color: white !important;
    box-shadow: 0 0 15px #ff0055 !important;
}
.stLinkButton > a {
    background-color: #111724 !important;
    color: #00f0ff !important;
    border: 1px solid #00f0ff !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    width: 100% !important;
    transition: 0.3s !important;
}
.stLinkButton > a:hover {
    background-color: #00f0ff !important;
    color: #000000 !important;
    box-shadow: 0 0 15px #00f0ff !important;
}
[data-testid="stChatInput"]:focus-within {
    border: 1px solid #00f0ff !important;
    box-shadow: 0 0 15px #00f0ff !important;
}
[data-testid="stFileUploaderDropzone"] {
    background-color: #111724 !important;
    border: 2px solid #00f0ff !important;
    border-radius: 12px !important;
}
[data-testid="stChatMessage"] {
    border: 1px solid rgba(0,240,255,0.12);
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}
hr {
    border-color: #00f0ff !important;
    opacity: 0.3;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])

with col1:
    try:
        st.image("images.jpg", width=100)
    except Exception:
        st.write("🤖")

with col2:
    st.title("Arsalan's AI v1.0")
    st.caption("Made by Arsalan Ali Khan | Teenager Genius 😎")

st.write("---")

st.sidebar.title("🤖 Arsalan's AI")
st.sidebar.caption("Cyberpunk AI Assistant")

langs = st.sidebar.selectbox(
    "Voice Language Selector",
    ["English", "Urdu"]
)

st.sidebar.write("---")
st.sidebar.subheader("Image Analysis")

upl = st.sidebar.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"]
)

if upl:
    st.sidebar.image(upl, caption="Uploaded Image")

st.sidebar.write("---")
st.sidebar.header("Additional Utilities")

st.sidebar.link_button(
    "Calculator",
    "https://alikhan30795.github.io/Calculator-JS/"
)

st.sidebar.link_button(
    "Password Strength Checker",
    "https://alikhan30795.github.io/psc/"
)

st.sidebar.link_button(
    "Tables Generator",
    "https://alikhan30795.github.io/Tables/"
)

st.sidebar.link_button(
    "Guessing Game",
    "https://alikhan30795.github.io/Guess/"
)

st.sidebar.write("---")
st.sidebar.header("AI Results in Coding")

st.sidebar.link_button(
    "Website Development",
    "https://arsalan-store-e9ux4x9n2-alikhan30795.vercel.app/"
)

st.sidebar.write("---")
st.sidebar.header("Chat Management")

if st.sidebar.button("Clear Chat 🗑️"):
    st.session_state.memory = []
    st.rerun()

st.sidebar.write("---")
st.sidebar.header("Developer Info")
st.sidebar.write("Created by Arsalan Ali Khan")
st.sidebar.write("9th Class Genius 😎")
st.sidebar.write("Version: 1.0")
st.sidebar.caption("Powered by Google Gemini")

def create_voice(text, language):
    try:
        lang_code = "ur" if language == "Urdu" else "en"
        audio_buffer = BytesIO()
        tts = gTTS(text=text, lang=lang_code)
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
    except Exception as e:
        st.warning(f"Voice Error: {e}")
        return None

def ask_gemini(prompt, uploaded_image=None, audio_file=None):

    history = []

    for item in st.session_state.memory[:-1]:

        if item["role"] == "User":
            history.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=item["text"])]
                )
            )

        elif item["role"] == "AI":
            history.append(
                types.Content(
                    role="model",
                    parts=[types.Part(text=item["text"])]
                )
            )

    chat = client.chats.create(
        model=MODEL,
        history=history,
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are Arsalan's AI, created by Arsalan Ali Khan. "
                "You are intelligent, friendly and helpful. "
                "Understand text, images and audio. "
                "Analyze user audio directly, understand spoken words, "
                "questions, language, tone and requests. "
                "If the user speaks Urdu or Roman Urdu, respond in "
                "the same language. If the user asks for transcription, "
                "provide the transcription. Never invent unclear audio. "
                "Help with programming, education, gaming, creativity "
                "and general knowledge."
            )
        )
    )

    message_content = [prompt]

    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert("RGB")
        message_content.append(image)

    if audio_file is not None:
        audio_part = types.Part.from_bytes(
            data=audio_file.getvalue(),
            mime_type=audio_file.type or "audio/wav"
        )
        message_content.append(audio_part)
        message_content.append(
            "Listen to and analyze this audio. Understand what "
            "the user says and respond to their request. "
            "Transcribe it if requested."
        )

    response = chat.send_message(message=message_content)

    return response.text or "Sorry, I could not generate a response."

def process_message(user_text, image_file=None, audio_file=None):

    if not user_text.strip() and image_file is None and audio_file is None:
        st.warning("Please enter text, upload an image or record audio.")
        return

    display_text = user_text.strip()

    if not display_text:
        display_text = "🎤 Audio message"

    image_bytes = image_file.getvalue() if image_file else None
    audio_bytes = audio_file.getvalue() if audio_file else None

    st.session_state.memory.append({
        "role": "User",
        "text": display_text,
        "image": image_bytes,
        "user_audio": audio_bytes
    })

    creator_questions = [
        "who are you",
        "made you",
        "creator",
        "owner",
        "tum kon ho",
        "kisne banaya",
        "kis ne banaya",
        "kis ne bnaya",
        "tumhe kisne",
        "tumhe kis ne"
    ]

    try:
        with st.spinner("Arsalan's AI is thinking..."):

            if any(word in display_text.lower() for word in creator_questions):
                reply = (
                    "Hello Buddy! I am Arsalan's AI. "
                    "A smart AI assistant programmed by genius "
                    "Arsalan Ali Khan. 😎"
                )
            else:
                reply = ask_gemini(
                    display_text,
                    image_file,
                    audio_file
                )

            audio_data = create_voice(reply, langs)

            st.session_state.memory.append({
                "role": "AI",
                "text": reply,
                "audio": audio_data
            })

        st.rerun()

    except Exception as e:
        st.error(f"AI Error: {e}")

with st.container():

    for chat in st.session_state.memory:

        if chat["role"] == "User":

            with st.chat_message("user"):
                st.markdown(chat["text"])

                if chat.get("image"):
                    st.image(chat["image"])

                if chat.get("user_audio"):
                    st.audio(
                        chat["user_audio"],
                        format="audio/wav"
                    )

        elif chat["role"] == "AI":

            with st.chat_message("assistant"):
                st.markdown(chat["text"])

                if chat.get("audio"):
                    st.audio(
                        chat["audio"],
                        format="audio/mp3"
                    )

prompt = st.chat_input(
    "Ask or speak to Arsalan's AI...",
    accept_audio=True,
    audio_sample_rate=16000
)

if prompt:

    user_text = prompt.text or ""
    audio_file = prompt.audio

    if user_text.strip() or audio_file:

        process_message(
            user_text,
            upl,
            audio_file
        )

