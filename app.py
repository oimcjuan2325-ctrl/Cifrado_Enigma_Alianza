import streamlit as st
import numpy as np

# --- CONFIGURACIÓN (ALFABETO DE 27) ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

ROTORES = {
    "I":   "EKMFLGDQVZNTOWÑYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOEÑ",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQOÑ"
}

# --- LÓGICA ---
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
    # Clavijero: Convertir string de clavijas en diccionario (ej: "AZ,BK")
    pares = {}
    if config['clavijas']:
        for par in config['clavijas'].upper().split(','):
            if len(par) == 2:
                pares[par[0]] = par[1]; pares[par[1]] = par[0]
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        res = "".join([pares.get(c, c) for c in texto_limpio])
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        res = aplicar_enigma_completo(res_hill, config)
    else:
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
if 'active_config' not in st.session_state: st.session_state.active_config = None

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
    st.title("🛡️ Sistema Cifrado Enigma de la Alianza")
    
    with st.expander("⚙️ Configuración de la Máquina", expanded=True):
        st.subheader("Rotores")
        c1, c2, c3 = st.columns(3)
        r1 = c1.selectbox("Rotor 1", ["I", "II", "III"])
        r2 = c2.selectbox("Rotor 2", ["I", "II", "III"])
        r3 = c3.selectbox("Rotor 3", ["I", "II", "III"])
        
        st.subheader("Posición Inicial")
        p1, p2, p3 = st.columns(3)
        pos1 = p1.selectbox("Posición R1", list(ALFABETO))
        pos2 = p2.selectbox("Posición R2", list(ALFABETO))
        pos3 = p3.selectbox("Posición R3", list(ALFABETO))
        
        st.subheader("Clavijas (Ej: AZ,BK)")
        clavijas = st.text_input("Escribe las parejas de clavijas:")
        
        if st.button("Confirmar Configuración"):
            st.session_state.active_config = {'r1':r1, 'r2':r2, 'r3':r3, 'p1':pos1, 'p2':pos2, 'p3':pos3, 'clavijas':clavijas}
            st.success("Configuración aplicada")

    if st.session_state.active_config:
        col_a, col_b = st.columns(2)
        with col_a:
            txt = st.text_input("Texto a cifrar:")
            if st.button("Cifrar"): st.code(procesar_total(txt, "cifrar", st.session_state.active_config))
        with col_b:
            code = st.text_input("Texto a descifrar:")
            if st.button("Descifrar"): st.code(procesar_total(code, "descifrar", st.session_state.active_config))
    
    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
