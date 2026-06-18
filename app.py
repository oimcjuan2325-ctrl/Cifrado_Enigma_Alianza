import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

ROTORES = {
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO"
}

# --- LÓGICA DE LA MÁQUINA ---
def aplicar_enigma_completo(texto, config, modo="cifrar"):
    # Configuración de rotores
    rot_izq = ROTORES[config['r1']]
    rot_cen = ROTORES[config['r2']]
    rot_der = ROTORES[config['r3']]
    pos = config['pos']
    
    res = ""
    for i, char in enumerate(texto):
        # Simulación de paso por 3 rotores
        idx = (MAPA_L_N[char] + pos + i) % 26
        # Pasada por los 3 (simplificado como permutación combinada)
        letra = rot_der[(MAPA_L_N[rot_cen[(MAPA_L_N[rot_izq[idx]] + i)%26]] + i)%26]
        res += letra
    return res

def procesar_total(texto, modo, config):
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # 1. Clavijero
        res = "".join([config['pares'].get(c, c) for c in texto_limpio])
        # 2. Hill
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        # 3. Enigma (3 rotores)
        res = aplicar_enigma_completo(res_hill, config, "cifrar")
    else:
        # Descifrado inverso
        res = aplicar_enigma_completo(texto_limpio, config, "descifrar")
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]]) # ¡Corregido el paréntesis aquí!
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            res_hill += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        res = "".join([config['pares'].get(c, c) for c in res_hill]).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios: res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ ---
st.set_page_config(layout="wide")
st.title("🛡️ Enigma Nazi-Hill Simulador")

# Sidebar: Configuración Enigma
st.sidebar.header("⚙️ Configuración Máquina")
c1, c2, c3 = st.sidebar.columns(3)
config = {
    'r1': c1.selectbox("R1", ["I", "II", "III"]),
    'r2': c2.selectbox("R2", ["II", "I", "III"]),
    'r3': c3.selectbox("R3", ["III", "II", "I"]),
    'pos': st.sidebar.slider("Posición Inicial", 0, 25, 0),
    'pares': {'A': 'Z', 'Z': 'A'} # Aquí puedes añadir más clavijas
}

col1, col2 = st.columns(2)
with col1:
    txt = st.text_input("Cifrar:")
    if st.button("Procesar Cifrado"): st.code(procesar_total(txt, "cifrar", config))
with col2:
    code = st.text_input("Descifrar:")
    if st.button("Procesar Descifrado"): st.code(procesar_total(code, "descifrar", config))
