import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Sistema de Cifrado", layout="wide")

# Abecedario
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CONV = {letra: i + 1 for i, letra in enumerate(ALFABETO)}

# --- LÓGICA DE CIFRADO ---
def procesar_frase(texto, modo):
    palabras = texto.upper().split()
    resultados = []
    for palabra in palabras:
        n = len(palabra)
        if modo == "cifrar":
            # Álgebra interna + César
            val = sum(CONV.get(palabra[i], 0) * (i + 1) for i in range(n))
            resultados.append(str(val + n))
        else:
            # Revertir César
            val_sin_cesar = int(palabra) - n
            resultados.append(str(val_sin_cesar))
    return " ".join(resultados)

# --- ESTADO DE SESIÓN ---
if 'logueado' not in st.session_state: st.session_state.logueado = False
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False

# --- INTERFAZ ---
st.title("🔐 Sistema de Cifrado")

if st.session_state.bloqueado:
    st.error("❌ Lo siento, hemos detectado que no eres un usuario apto para utilizar esta web.")
    st.warning("Por favor, espera a que termine la cuenta regresiva antes de poder utilizar otra vez el inicio de sesión.")
    
    placeholder = st.empty()
    for i in range(60, 0, -1):
        placeholder.metric("Tiempo restante para reintento:", f"{i} segundos")
        time.sleep(1)
    placeholder.write("Cuenta regresiva finalizada... pero el acceso sigue denegado por seguridad.")
    st.stop()

if not st.session_state.logueado:
    password = st.text_input("Introduce la contraseña:", type="password")
    if st.button("Iniciar sesión"):
        if password == "MAQUINA":
            st.session_state.logueado = True
            st.rerun()
        else:
            st.session_state.intentos += 1
            if st.session_state.intentos >= 3:
                st.session_state.bloqueado = True
                st.rerun()
            else:
                st.error(f"Palabra incorrecta. Por favor, inténtelo de nuevo. (Intento {st.session_state.intentos}/3)")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cifrar Mensaje")
        msg = st.text_input("Mensaje a cifrar:")
        if st.button("Cifrar"):
            if any(char.isdigit() for char in msg):
                st.error("Lo siento, pero esta web no puede procesar números para los cálculos. Por favor, escríbelos manualmente a base de letras.")
            else:
                st.code(procesar_frase(msg, "cifrar"))
    with col2:
        st.subheader("Descifrar Mensaje")
        cif_input = st.text_input("Texto cifrado:")
        if st.button("Descifrar"):
            if any(char.isalpha() for char in cif_input):
                st.error("Lo siento, pero esta web no puede procesar letras para el descifrado. Por favor, introduce solo el código numérico.")
            else:
                try:
                    st.code(procesar_frase(cif_input, "descifrar"))
                except:
                    st.error("Error al procesar el código. Verifique los datos.")

    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.session_state.intentos = 0
        st.rerun()
