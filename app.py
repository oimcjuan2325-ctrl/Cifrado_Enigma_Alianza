import streamlit as st
import numpy as np

# --- CONFIGURACIÓN (ALFABETO DE 27) ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
# Matriz de Hill 2x2 (invertible en módulo 27)
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# Rotores adaptados a 27 posiciones
ROTORES = {
    "I":   "EKMFLGDQVZNTOWÑYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOEÑ",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQOÑ"
}

# --- LÓGICA DE CIFRADO ---
def aplicar_enigma_completo(texto, config):
    rot_izq = ROTORES[config['r1']]
    rot_cen = ROTORES[config['r2']]
    rot_der = ROTORES[config['r3']]
    pos = [MAPA_L_N[config['p1']], MAPA_L_N[config['p2']], MAPA_L_N[config['p3']]]
    
    res = ""
    for i, char in enumerate(texto):
        idx = (MAPA_L_N[char] + pos[2] + i) % 27
        letra = rot_der[(MAPA_L_N[rot_cen[(MAPA_L_N[rot_izq[idx]] + i)%27]] + i)%27]
        res += letra
    return res

def procesar_total(texto, modo, config):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    pares = {config['c1']: config['c2'], config['c2']: config['c1']}
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # 1. Clavijero -> 2. Hill -> 3. Enigma
        res = "".join([pares.get(c, c) for c in texto_limpio])
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        res = aplicar_enigma_completo(res_hill, config)
    else:
        # Descifrado inverso
        res = aplicar_enigma_completo(texto_limpio, config)
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            res_hill += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        res = "".join([pares.get(c, c) for c in res_hill]).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios: res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma de la Alianza", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Inicio de sesión en la Enigma de la Alianza")
    pwd = st.text_input("Contraseña:", type="password")
    if st.button("Acceder"):
        if pwd == "MAQUINA":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.title("🛡️ Sistema Cifrado Enigma de la Alianza (Con Ñ)")
    
    st.sidebar.header("⚙️ Configuración Máquina")
    
    st.sidebar.subheader("Rotores")
    c1, c2, c3 = st.sidebar.columns(3)
    config = {
        'r1': c1.selectbox("R1", ["I", "II", "III"]),
        'r2': c2.selectbox("R2", ["II", "I", "III"]),
        'r3': c3.selectbox("R3", ["III", "II", "I"]),
    }
    
    st.sidebar.subheader("Posición Inicial")
    p1, p2, p3 = st.sidebar.columns(3)
    config['p1'] = p1.selectbox("P1", list(ALFABETO))
    config['p2'] = p2.selectbox("P2", list(ALFABETO))
    config['p3'] = p3.selectbox("P3", list(ALFABETO))
    
    st.sidebar.subheader("Clavijero (Steckerbrett)")
    col_c1, col_c2 = st.sidebar.columns(2)
    config['c1'] = col_c1.selectbox("Clavija 1", list(ALFABETO))
    config['c2'] = col_c2.selectbox("Clavija 2", list(ALFABETO))
    
    col_cif, col_des = st.columns(2)
    with col_cif:
        txt = st.text_input("Texto a cifrar:")
        if st.button("Cifrar"): st.code(procesar_total(txt, "cifrar", config))
    with col_des:
        code = st.text_input("Texto a descifrar:")
        if st.button("Descifrar"): st.code(procesar_total(code, "descifrar", config))
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
