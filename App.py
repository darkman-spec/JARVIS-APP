import streamlit as st
from google import genai
from google.genai import types
from gtts import gTTS
import os

# Configuration de la page
st.set_page_config(page_title="JARVIS AI", page_icon="⚡", layout="centered")

# Style CSS futuriste
st.markdown("""
    <style>
    .stApp {
        background-color: #050b14;
        color: #00f3ff;
    }
    h1 {
        text-align: center;
        font-family: monospace;
        color: #00f3ff;
        text-shadow: 0px 0px 10px #00f3ff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>J.A.R.V.I.S.</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8a99ad;'>Système opérationnel - Permanent</p>", unsafe_allow_html=True)

# Affichage de l'Arc Reactor visuel
st.image("https://i.imgur.com/3Z66p9u.gif", width=150)

# Récupération sécurisée de la clé API depuis Render
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("⚠️ La variable d'environnement GEMINI_API_KEY n'est pas configurée dans Render.")
else:
    client = genai.Client(api_key=API_KEY)

    # Initialisation de l'historique
    if "messages" not in st.session_state:
        st.session_state.messages = []

    system_instruction = "Tu es JARVIS, l'assistant IA de Tony Stark. Réponds toujours en français, de manière très concise (1-2 phrases), polie et avec une touche d'esprit."

    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie
    if prompt := st.chat_input("Donnez un ordre à JARVIS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                chat = client.chats.create(
                    model="gemini-3.6-flash",
                    config=types.GenerateContentConfig(system_instruction=system_instruction)
                )
                response = chat.send_message(prompt)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

                # Synthèse vocale
                tts = gTTS(text=answer, lang='fr', tld='fr')
                tts.save("response.mp3")
                st.audio("response.mp3", autoplay=True)
            except Exception as e:
                st.error(f"Erreur système : {e}")
