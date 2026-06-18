import streamlit as st
import numpy as np

# --- CONFIGURACIÓN DEL SISTEMA ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}

# Matriz de Hill 2x2: [[3, 2], [1, 1]]
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
# Inversa de la matriz módulo 27: [[1, 25], [26, 3]]
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# --- LÓGICA DE MÁQUINA ENIGMA (ROTOR) ---
def aplicar_rotor(texto, posicion):
    resultado = ""
    for i, letra in enumerate(texto):
        idx = (MAPA_L_N[letra] + posicion + i) % 27
        resultado += MAPA_N_L[idx]
    return resultado

def revertir_rotor(texto, posicion):
    resultado = ""
    for i, letra in enumerate(texto):
        idx = (MAPA_L_N[letra] - posicion - i) % 27
        resultado += MAPA_N_L[idx]
    return resultado

# --- LÓGICA HILL ---
def cifrar_hill(texto):
    texto = "".join([c for c in texto.upper() if c in ALFABETO])
    if len(texto) % 2 != 0: texto += "X"
    # Capa 1: Enigma (Rotor)
    texto = aplicar_rotor(texto, 3) 
    # Capa 2: Hill
    nums = [MAPA_L_N[c] for c in texto]
    resultado = ""
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        cifrado = np.dot(MATRIZ_HILL, vector) % 27
        resultado += MAPA_N_L[cifrado[0]] + MAPA_N_L[cifrado[1]]
    return resultado

def descifrar_hill(texto_cifrado):
    nums = [MAPA_L_N[c] for c in texto_cifrado.upper() if c in ALFABETO]
    # Capa 2 inversa: Hill
    texto_intermedio = ""
    for i in range(0, len(nums), 2):
        vector = np.array([nums[i], nums[i+1]])
        descifrado = np.dot(MATRIZ_INVERSA, vector) % 27
        texto_intermedio += MAPA_N_L[descifrado[0]] + MAPA_N_L[descifrado[1]]
    # Capa 1 inversa: Enigma
    return revertir_rotor(texto_intermedio, 3).replace("X", "")

# --- INTERFAZ WEB (STREAMLIT) ---
st.set_page_config(page_title="Cifrado Enigma Dual", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acceso a Enigma")
    pwd = st.text_input("Palabra clave:", type="password")
    if st.button("Iniciar sesión"):
        if pwd == "MAQUINA":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.title("🛡️ Sistema Cifrado Enigma Dual")
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📤 Cifrar")
        txt = st.text_input("Texto original:")
        if st.button("Ejecutar Cifrado"):
            if txt:
                st.success(f"Resultado: {cifrar_hill(txt)}")
            else:
                st.warning("Escribe algo para cifrar.")

    with col2:
        st.header("📥 Descifrar")
        code = st.text_input("Código a descifrar:")
        if st.button("Ejecutar Descifrado"):
            if code:
                st.info(f"Mensaje original: {descifrar_hill(code)}")
            else:
                st.warning("Escribe un código para descifrar.")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
