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

# --- LÓGICA DE CIFRADO ---
def generar_abecedario_maquina(config):
    """Crea una tabla de sustitución única para la configuración actual."""
    rot_izq, rot_cen, rot_der = ROTORES[config['r1']], ROTORES[config['r2']], ROTORES[config['r3']]
    pos = [MAPA_L_N[config['p1']], MAPA_L_N[config['p2']], MAPA_L_N[config['p3']]]
    
    mapeo = {}
    for char in ALFABETO:
        idx = (MAPA_L_N[char] + pos[2]) % 27
        mapeo[char] = rot_der[(MAPA_L_N[rot_cen[(MAPA_L_N[rot_izq[idx]])%27]] )%27]
    return mapeo

def procesar_total(texto, modo, config):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    # 1. Aplicar Clavijero
    pares = {}
    if config['clavijas']:
        for par in config['clavijas'].upper().split(','):
            if len(par.strip()) == 2:
                p = par.strip()
                pares[p[0]] = p[1]; pares[p[1]] = p[0]
    
    # 2. Aplicar abecedario único de la máquina (Enigma)
    mapeo = config['abecedario']
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # Paso 1: Clavijero
        temp = "".join([pares.get(c, c) for c in texto_limpio])
        # Paso 2: Hill
        res_hill = ""
        for i in range(0, len(temp), 2):
            vec = np.array([MAPA_L_N[temp[i]], MAPA_L_N[temp[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        # Paso 3: Enigma (Sustitución única)
        res = "".join([mapeo[c] for c in res_hill])
    else:
        # Descifrado inverso
        # Paso 3 inv: Inversa Enigma
        mapeo_inv = {v: k for k, v in mapeo.items()}
        temp = "".join([mapeo_inv[c] for c in texto_limpio])
        # Paso 2 inv: Inversa Hill
        res_hill = ""
        for i in range(0, len(temp), 2):
            vec = np.array([MAPA_L_N[temp[i]], MAPA_L_N[temp[i+1]]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            res_hill += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        # Paso 1 inv: Inverso Clavijero
        res = "".join([pares.get(c, c) for c in res_hill]).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios:
        if pos < len(res_lista): res_lista.insert(pos, " ")
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
    st.title("🛡️ Sistema Cifrado Enigma de la Alianza")
    
    with st.expander("⚙️ Configuración de la Máquina", expanded=True):
        st.subheader("Rotores")
        c1, c2, c3 = st.columns(3)
        r1, r2, r3 = c1.selectbox("R1", ["I", "II", "III"]), c2.selectbox("R2", ["II", "I", "III"]), c3.selectbox("R3", ["III", "II", "I"])
        
        st.subheader("Posición Inicial")
        p1, p2, p3 = st.columns(3)
        pos1, pos2, pos3 = p1.selectbox("P1", list(ALFABETO)), p2.selectbox("P2", list(ALFABETO)), p3.selectbox("P3", list(ALFABETO))
        
        clavijas = st.text_input("Clavijas (Ej: AZ,BK):")
        
        if st.button("Confirmar Configuración"):
            conf = {'r1':r1, 'r2':r2, 'r3':r3, 'p1':pos1, 'p2':pos2, 'p3':pos3, 'clavijas':clavijas}
            st.session_state.active_config = conf
            st.session_state.active_config['abecedario'] = generar_abecedario_maquina(conf)
            st.success("Configuración aplicada: Abecedario único generado.")

    if 'active_config' in st.session_state and st.session_state.active_config:
        col_a, col_b = st.columns(2)
        with col_a:
            txt = st.text_input("Texto a cifrar:")
            if st.button("Cifrar"): st.code(procesar_total(txt, "cifrar", st.session_state.active_config))
        with col_b:
            code = st.text_input("Texto a descifrar:")
            if st.button("Descifrar"): st.code(procesar_total(code, "descifrar", st.session_state.active_config))
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
