import streamlit as st
import time

# --- FUNCIONES DE CIFRADO ---
def cifrar_mensaje(mensaje):
    n = len(mensaje)
    resultado = ""
    for i, char in enumerate(mensaje, 1):
        # Valor original (A=1, B=2...)
        vi = ord(char.upper()) - 64 
        # Fórmula: Ci = (Vi + 2*i + n + n) mod 27 
        # (Usamos 2n porque sumamos n de la fórmula original + n del César)
        ci = (vi + (2 * i) + (2 * n)) % 27
        if ci == 0: ci = 27
        resultado += chr(ci + 64)
    return resultado

# --- INTERFAZ Y LÓGICA DE ACCESO ---
st.set_page_config(page_title="Sistema de Cifrado")
st.title("🔒 Sistema de Cifrado")

# Lógica de estados... (mantén la lógica de intentos y bloqueo que te pasé antes)

if st.session_state.get('autenticado', False):
    st.subheader("Herramienta de Cifrado")
    mensaje_input = st.text_input("Mensaje a cifrar:")
    
    if st.button("Ejecutar Cifrado"):
        if mensaje_input:
            cifrado = cifrar_mensaje(mensaje_input)
            st.success(f"Resultado: {cifrado}")
        else:
            st.warning("Por favor, introduce un texto.")
