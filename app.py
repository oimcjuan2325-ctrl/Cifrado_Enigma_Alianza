import streamlit as st
import time

# Configuración de página
st.set_page_config(page_title="Sistema de Cifrado", layout="wide")

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CONV = {letra: i + 1 for i, letra in enumerate(ALFABETO)}
INV_CONV = {i + 1: letra for i, letra in enumerate(ALFABETO)}

# --- LÓGICA DE CIFRADO POR LETRAS ---
def transformar_frase(texto, modo):
    texto = texto.upper().replace(" ", "")
    resultado = ""
    n = len(texto)
    
    for i in range(n):
        letra = texto[i]
        valor_letra = CONV.get(letra, 0)
        
        if modo == "cifrar":
            # Aplicamos el álgebra: (valor + posición + n) % 27
            nuevo_valor = (valor_letra + (i + 1) + n) % 27
            resultado += INV_CONV.get(nuevo_valor if nuevo_valor != 0 else 27, "A")
        else:
            # Revertimos la operación
            valor_original = (valor_letra - (i + 1) - n) % 27
            resultado += INV_CONV.get(valor_original if valor_original != 0 else 27, "A")
            
    return resultado

# --- ESTADO DE SESIÓN ---
if 'logueado' not in st.session_state: st.session_state.logueado = False
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False

# --- INTERFAZ ---
st.title("🔐 Sistema de Cifrado")

if st.session_state.bloqueado:
    st.error("❌ Lo siento, hemos detectado que no eres un usuario apto para utilizar esta web.")
    placeholder = st.empty()
    for i in range(60, 0, -1):
        placeholder.metric("Tiempo restante:", f"{i} segundos")
        time.sleep(1)
    placeholder.write("Cuenta regresiva finalizada... pero el acceso sigue denegado.")
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
            st.error("Palabra incorrecta. Inténtelo de nuevo.")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cifrar Mensaje")
        msg = st.text_input("Mensaje a cifrar:")
        if st.button("Cifrar"):
            st.code(transformar_frase(msg, "cifrar"))
    with col2:
        st.subheader("Descifrar Mensaje")
        cif_input = st.text_input("Texto cifrado:")
        if st.button("Descifrar"):
            st.code(transformar_frase(cif_input, "descifrar"))

    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.session_state.intentos = 0
        st.rerun()
