import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

# ✅ Your API Key (keep private)
OPENROUTER_API_KEY = "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"

# 🚀 Query OpenRouter AI
def ask_openrouter(question):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are Rolex, an intelligent, confident and deeply knowledgeable AI assistant with a strong masculine personality. Always reply to the user's question like a professional assistant."},
            {"role": "user", "content": question}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        elif "error" in result:
            return f"API Error: {result['error']['message']}"
        else:
            return "Unexpected API response."
    except Exception as e:
        return f"Error: {str(e)}"

# 🎤 Mic input
def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand you."
    except sr.RequestError:
        return "Network error."

# 🔊 Voice output (deep male)
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 135)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "david" in voice.name.lower() or "mark" in voice.name.lower() or "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

# 🌐 Streamlit UI Config
st.set_page_config(page_title="Rolex AI", page_icon="🤖", layout="centered")

# 💄 Custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(to top right, #0f172a, #1e293b);
        color: #e2e8f0;
    }
    .stApp {
        background-color: #0f172a;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2 {
        text-align: center;
        color: #38bdf8;
        text-shadow: 0 0 15px #0ea5e9;
    }
    .stButton button {
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        box-shadow: 0 0 20px #0ea5e9;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #0ea5e9;
        box-shadow: 0 0 30px #38bdf8;
    }
    .stTextInput>div>div>input {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Header
st.markdown("<h1>🤖 Rolex - Your Personal AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h2>Speak. Ask. Command.</h2>", unsafe_allow_html=True)

# 🎛 Input selection
mode = st.radio("Choose input method:", ["🎤 Voice", "⌨️ Text"], horizontal=True)

if mode == "🎤 Voice":
    if st.button("🎙 Start Listening"):
        user_input = listen_to_mic()
        st.text_area("🧏 You said:", user_input, height=80)
        if user_input.strip():
            with st.spinner("🧠 Thinking..."):
                answer = ask_openrouter(user_input)
            st.success(answer)
            speak(answer)

elif mode == "⌨️ Text":
    user_input = st.text_input("Type your question:")
    if st.button("💬 Get Answer"):
        if user_input.strip():
            with st.spinner("🧠 Thinking..."):
                answer = ask_openrouter(user_input)
            st.success(answer)
            speak(answer)

# 📎 Footer
st.markdown("""
    <hr style="border: 1px solid #334155;">
    <p style='text-align:center;color:#64748b;'>⚙️ Rolex AI | Built with 💡 by <strong>Prasad Ghavghave</strong></p>
""", unsafe_allow_html=True)
