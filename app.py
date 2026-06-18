import streamlit as st
import numpy as np

# --- CONFIGURACIÓN (ALFABETO DE 27) ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
# Matriz de Hill 2x2
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

ROTORES = {
    "I":   "EKMFLGDQVZNTOWÑYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOEÑ",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQOÑ"
}

# --- LÓGICA: GENERACIÓN DE ABECEDARIO ÚNICO ---
def generar_abecedario_unico(config):
    """
    Simula el paso de cada letra por la configuración de rotores y 
    devuelve un diccionario que actúa como el abecedario de esa máquina.
    """
    rot1, rot2, rot3 = ROTORES[config['r1']], ROTORES[config['r2']], ROTORES[config['r3']]
    p1, p2, p3 = MAPA_L_N[config['p1']], MAPA_L_N[config['p2']], MAPA_L_N[config['p3']]
    
    mapeo = {}
    for char in ALFABETO:
        # Trayectoria: Letra -> R3 -> R2 -> R1
        i = MAPA_L_N[char]
        # Aplicamos la posición de cada rotor como desfase
        paso3 = rot3[(i + p3) % 27]
        paso2 = rot2[(MAPA_L_N[paso3] + p2) % 27]
        paso1 = rot1[(MAPA_L_N[paso2] + p1) % 27]
        mapeo[char] = paso1
    return mapeo

# --- PROCESAMIENTO TOTAL ---
def procesar_total(texto, modo, config):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    # Clavijero
    pares = {c: c for c in ALFABETO}
    if config['clavijas']:
        for par in config['clavijas'].upper().split(','):
            if len(par.strip()) == 2:
                p = par.strip()
                pares[p[0]] = p[1]; pares[p[1]] = p[0]
    
    mapeo = config['abecedario']
    mapeo_inv = {v: k for k, v in mapeo.items()}

    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # FLUJO: Clavijero -> Enigma (Abecedario Único) -> Hill
        t = "".join([pares[c] for c in texto_limpio])
        t = "".join([mapeo[c] for c in t])
        res = ""
        for i in range(0, len(t), 2):
            vec = np.array([MAPA_L_N[t[i]], MAPA_L_N[t[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
    else:
        # FLUJO INVERSO: Hill -> Enigma -> Clavijero
        t = ""
        for i in range(0, len(texto_limpio), 2):
            vec = np.array([MAPA_L_N[texto_limpio[i]], MAPA_L_N[texto_limpio[i+1]]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            t += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        t = "".join([mapeo_inv[c] for c in t])
        res = "".join([pares[c] for c in t]).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios:
        if pos < len(res_lista): res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma de la Alianza", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Inicio de sesión en la Enigma de la Alianza")
    if st.text_input("Contraseña:", type="password") == "MAQUINA":
        st.session_state.logged_in = True
        st.rerun()
else:
    st.title("🛡️ Sistema Cifrado Enigma de la Alianza")
    
    with st.expander("⚙️ Configuración de la Máquina", expanded=True):
        c1, c2, c3 = st.columns(3)
        r1 = c1.selectbox("Rotor 1", ["I", "II", "III"])
        r2 = c2.selectbox("Rotor 2", ["I", "II", "III"])
        r3 = c3.selectbox("Rotor 3", ["I", "II", "III"])
        
        c4, c5, c6 = st.columns(3)
        p1 = c4.selectbox("Pos R1", list(ALFABETO))
        p2 = c5.selectbox("Pos R2", list(ALFABETO))
        p3 = c6.selectbox("Pos R3", list(ALFABETO))
        
        clavijas = st.text_input("Clavijas (Ej: AZ,BK):")
        
        if st.button("Confirmar Configuración"):
            conf = {'r1':r1, 'r2':r2, 'r3':r3, 'p1':p1, 'p2':p2, 'p3':p3, 'clavijas':clavijas}
            # AQUÍ OCURRE LA MAGIA: Cada combinación genera su mapa único
            conf['abecedario'] = generar_abecedario_unico(conf)
            st.session_state.active_config = conf
            st.success("Configuración aplicada: Abecedario de sustitución generado para esta combinación.")

    if 'active_config' in st.session_state and st.session_state.active_config:
        col_a, col_b = st.columns(2)
        txt = col_a.text_input("Texto a cifrar:")
        if col_a.button("Cifrar"): col_a.code(procesar_total(txt, "cifrar", st.session_state.active_config))
        code = col_b.text_input("Texto a descifrar:")
        if col_b.button("Descifrar"): col_b.code(procesar_total(code, "descifrar", st.session_state.active_config))
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.rerun()
