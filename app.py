import streamlit as st
import numpy as np

# --- LÓGICA DE ENIGMA (Integrada en app.py) ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])

def cifrar_hill(texto):
    texto = "".join([c for c in texto.upper() if c in ALFABETO])
    if len(texto) % 2 != 0: texto += "X"
    nums = [MAPA_L_N[c] for c in texto]
    resultado = ""
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        cifrado = np.dot(MATRIZ_HILL, vector) % 27
        resultado += MAPA_N_L[cifrado[0]] + MAPA_N_L[cifrado[1]]
    return resultado

def descifrar_hill(texto_cifrado):
    inv_matriz = np.array([[1, 25], [26, 3]])
    nums = [MAPA_L_N[c] for c in texto_cifrado.upper()]
    resultado = ""
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        descifrado = np.dot(inv_matriz, vector) % 27
        resultado += MAPA_N_L[descifrado[0]] + MAPA_N_L[descifrado[1]]
    return resultado.replace("X", "")

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Cifrado Enigma", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acceso a Enigma")
    pwd = st.text_input("Palabra clave:", type="password")
    if st.button("Iniciar sesión"):
        if pwd == "máquina":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.title("🛡️ Sistema Cifrado Enigma")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Cifrar")
        txt = st.text_input("Texto original:")
        if st.button("Cifrar"):
            st.success(f"Resultado: {cifrar_hill(txt)}")

    with col2:
        st.header("Descifrar")
        code = st.text_input("Código a descifrar:")
        if st.button("Descifrar"):
            st.info(f"Mensaje original: {descifrar_hill(code)}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
