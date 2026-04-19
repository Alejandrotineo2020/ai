import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configuración de la página
st.set_page_config(page_title="Mi Mini AI", page_icon="🤖")
st.title("🤖 Mi Asistente Personal")

# Cargar API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# --- BUSCADOR AUTOMÁTICO DE MODELOS ---
@st.cache_resource
def obtener_modelo():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return "gemini-pro" # Fallback

modelo_nombre = obtener_modelo()
model = genai.GenerativeModel(modelo_nombre)
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Forzamos la respuesta
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error con el modelo {modelo_nombre}: {e}")