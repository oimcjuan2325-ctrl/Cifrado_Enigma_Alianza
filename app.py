import streamlit as st
import numpy as np
import datetime

# --- CONFIGURACIÓN ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# --- LÓGICA DE CIFRADO ---
def aplicar_cesar_fecha(texto, modo="cifrar"):
    # El desplazamiento se basa en el día y mes actual
    hoy = datetime.date.today()
    desplazamiento = hoy.day + hoy.month
    res = ""
    for char in texto.upper():
        if char in ALFABETO:
            idx = MAPA_L_N[char]
            if modo == "cifrar":
                nuevo_idx = (idx + desplazamiento) % 27
            else:
                nuevo_idx = (idx - desplazamiento) % 27
            res += MAPA_N_L[nuevo_idx]
        else:
            res += char
    return res

def procesar_total(texto, modo):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # 1. César por fecha -> 2. Hill
        temp = aplicar_cesar_fecha(texto_limpio, "cifrar")
        res = ""
        for i in range(0, len(temp), 2):
            vec = np.array([MAPA_L_N[temp[i]], MAPA_L_N[temp[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
    else:
        # 1. Hill Inversa -> 2. César por fecha Inverso
        temp = ""
        for i in range(0, len(texto_limpio), 2):
            vec = np.array([MAPA_L_N[texto_limpio[i]], MAPA_L_N[texto_limpio[i+1]]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            temp += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        res = aplicar_cesar_fecha(temp, "descifrar").replace("X", "")
        
    res_lista = list(res)
    for pos in espacios:
        if pos < len(res_lista): res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(page_title="Cifrado Alianza", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Inicio de sesión en la Alianza")
    pwd = st.text_input("Contraseña:", type="password")
    if st.button("Acceder"):
        if pwd == "MAQUINA":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.title("🛡️ Sistema Cifrado: César + Hill")
    st.write(f"**Fecha clave activa:** {datetime.date.today().strftime('%d/%m')}")
    
    col_cif, col_des = st.columns(2)
    
    with col_cif:
        txt = st.text_input("Texto a cifrar:")
        if st.button("Cifrar"):
            st.code(procesar_total(txt, "cifrar"))
            
    with col_des:
        code = st.text_input("Texto a descifrar:")
        if st.button("Descifrar"):
            st.code(procesar_total(code, "descifrar"))
            
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
