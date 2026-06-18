import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# --- LÓGICA DE ROTORES (Simulación) ---
# Cada rotor es una permutación distinta del alfabeto
ROTORES = {
    "I":  "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO"
}

def aplicar_rotor_enigma(texto, rotor_nombre, posicion, modo="cifrar"):
    rotor_map = ROTORES[rotor_nombre]
    resultado = ""
    for i, char in enumerate(texto):
        idx_entrada = (MAPA_L_N[char] + posicion + i) % 27
        letra_mapeada = rotor_map[idx_entrada % 26] if idx_entrada < 26 else char
        resultado += letra_mapeada
    return resultado

# --- LÓGICA PRINCIPAL ---
def procesar_total(texto, modo, config):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    # Extraer configuración
    pares = config['pares']
    rotor = config['rotor']
    pos = config['posicion']

    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # 1. Clavijero -> 2. Hill -> 3. Rotor
        res = "".join([pares.get(c, c) for c in texto_limpio])
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        res = aplicar_rotor_enigma(res_hill, rotor, pos, "cifrar")
    else:
        # Descifrar: Inverso (Rotor -> Hill -> Clavijero)
        res = aplicar_rotor_enigma(texto_limpio, rotor, pos, "descifrar")
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array(MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            res_hill += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        res = "".join([pares.get(c, c) for c in res_hill]).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios: res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Nazi-Hill Pro", layout="wide")

if 'config' not in st.session_state:
    st.session_state.config = {'rotor': 'I', 'posicion': 0, 'pares': {'A': 'Z', 'Z': 'A'}}

st.sidebar.title("⚙️ Ajustes Enigma")
st.session_state.config['rotor'] = st.sidebar.selectbox("Seleccionar Rotor:", ["I", "II", "III"])
st.session_state.config['posicion'] = st.sidebar.slider("Posición inicial:", 0, 25, 0)
p1 = st.sidebar.text_input("Clavija 1 (Letra):", "A").upper()
p2 = st.sidebar.text_input("Clavija 2 (Letra):", "Z").upper()
st.session_state.config['pares'] = {p1: p2, p2: p1}

st.title("🛡️ Sistema Cifrado Enigma Dual")
col1, col2 = st.columns(2)
with col1:
    txt = st.text_input("Texto:")
    if st.button("Cifrar"): st.code(procesar_total(txt, "cifrar", st.session_state.config))
with col2:
    code = st.text_input("Código:")
    if st.button("Descifrar"): st.code(procesar_total(code, "descifrar", st.session_state.config))
