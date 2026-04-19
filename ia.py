import os
import google.generativeai as genai
from dotenv import load_dotenv

# Configuración
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERROR: No se encontró la API Key en el archivo .env")
    exit()

genai.configure(api_key=api_key)

# Configurar el modelo
model = genai.GenerativeModel('gemini-1.5-flash')

def chat():
    print("✅ IA CONECTADA. Escribe algo para comenzar...")
    sesion = model.start_chat(history=[])
    
    while True:
        usuario = input("\nUsuario: ")
        if usuario.lower() in ['salir', 'exit']:
            break
            
        try:
            response = sesion.send_message(usuario)
            print(f"\nAI: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat()