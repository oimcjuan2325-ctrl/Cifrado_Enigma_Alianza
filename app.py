import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# --- LÓGICA DE CIFRADO ---
def procesar_texto(texto, modo="cifrar"):
    # Guardamos las posiciones de los espacios
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    if modo == "cifrar":
        # Relleno si es impar
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # Capa 1: Rotor
        texto_tmp = "".join([MAPA_N_L[(MAPA_L_N[c] + 3 + i) % 27] for i, c in enumerate(texto_limpio)])
        # Capa 2: Hill
        res = ""
        for i in range(0, len(texto_tmp), 2):
            vec = np.array([MAPA_L_N[texto_tmp[i]], MAPA_L_N[texto_tmp[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
    else:
        # Descifrar Hill
        nums = [MAPA_L_N[c] for c in texto_limpio]
        texto_tmp = ""
        for i in range(0, len(nums), 2):
            vec = np.array([nums[i], nums[i+1]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            texto_tmp += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        # Revertir Rotor
        res = "".join([MAPA_N_L[(MAPA_L_N[c] - 3 - i) % 27] for i, c in enumerate(texto_tmp)])
        res = res.replace("X", "")
        
    # Reinsertar espacios en sus posiciones originales
    res_lista = list(res)
    for pos in espacios:
        res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Dual", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acceso a Enigma")
    pwd = st.text_input("Palabra clave:", type="password")
    if st.button("Iniciar sesión"):
        if pwd == "máquina":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.title("🛡️ Sistema Cifrado Enigma Dual")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📤 Cifrar")
        txt = st.text_input("Texto original:")
        if st.button("Ejecutar Cifrado"):
            if txt:
                st.success("Resultado:")
                st.code(procesar_texto(txt, "cifrar"))

    with col2:
        st.header("📥 Descifrar")
        code = st.text_input("Código a descifrar:")
        if st.button("Ejecutar Descifrado"):
            if code:
                st.info("Mensaje original:")
                st.code(procesar_texto(code, "descifrar"))

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
