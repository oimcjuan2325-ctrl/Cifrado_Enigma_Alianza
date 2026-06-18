import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MAPA_L_N = {l: i for i, l in enumerate(ALFABETO)}
MAPA_N_L = {i: l for i, l in enumerate(ALFABETO)}
# Matriz de Hill 2x2 predefinida
MATRIZ_HILL = np.array([[3, 2], [1, 1]])
MATRIZ_INVERSA = np.array([[1, 25], [26, 3]])

# --- FUNCIONES CRIPTOGRÁFICAS ---
def aplicar_clavijero(texto, pares):
    """Intercambia letras según el tablero de clavijas."""
    return "".join([pares.get(c, c) for c in texto])

def aplicar_rotor(texto, pos, modo="cifrar"):
    """Aplica el desplazamiento de rotor (Simulación de Enigma)."""
    desplazamiento = pos if modo == "cifrar" else -pos
    return "".join([MAPA_N_L[(MAPA_L_N[c] + desplazamiento + i) % 27] for i, c in enumerate(texto)])

def procesar_total(texto, modo, pares):
    """Procesa el mensaje completo a través de las 3 capas de seguridad."""
    espacios = [i for i, char in enumerate(texto) if char == " "]
    texto_limpio = "".join([c for c in texto.upper() if c in ALFABETO])
    
    if modo == "cifrar":
        if len(texto_limpio) % 2 != 0: texto_limpio += "X"
        # 1. Clavijero -> 2. Hill -> 3. Rotor
        res = aplicar_clavijero(texto_limpio, pares)
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            cif = np.dot(MATRIZ_HILL, vec) % 27
            res_hill += MAPA_N_L[cif[0]] + MAPA_N_L[cif[1]]
        res = aplicar_rotor(res_hill, 3, "cifrar")
    else:
        # Descifrar: Inverso del orden (Rotor -> Hill -> Clavijero)
        # 1. Inverso Rotor
        res = aplicar_rotor(texto_limpio, 3, "descifrar")
        # 2. Inverso Hill
        res_hill = ""
        for i in range(0, len(res), 2):
            vec = np.array([MAPA_L_N[res[i]], MAPA_L_N[res[i+1]]])
            des = np.dot(MATRIZ_INVERSA, vec) % 27
            res_hill += MAPA_N_L[des[0]] + MAPA_N_L[des[1]]
        # 3. Inverso Clavijero
        res = aplicar_clavijero(res_hill, pares).replace("X", "")
        
    res_lista = list(res)
    for pos in espacios: res_lista.insert(pos, " ")
    return "".join(res_lista)

# --- INTERFAZ WEB ---
st.set_page_config(page_title="Enigma Dual Pro", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'pares' not in st.session_state: st.session_state.pares = {'A': 'Z', 'Z': 'A'}

if not st.session_state.logged_in:
    st.title("🔐 Acceso a la Central Enigma")
    if st.button("Iniciar Operaciones"): st.session_state.logged_in = True; st.rerun()
else:
    st.sidebar.title("🛠️ Panel de Control")
    st.title("🛡️ Sistema Cifrado Enigma Dual (Multi-Capa)")
    
    tab1, tab2 = st.tabs(["📤/📥 Procesar", "⚙️ Configuración del Clavijero"])
    
    with tab2:
        st.header("Configuración de Seguridad")
        c1, c2 = st.columns(2)
        p1 = c1.text_input("Conectar letra (ej: A):", "A").upper()
        p2 = c2.text_input("Conectar con (ej: Z):", "Z").upper()
        if st.button("Guardar Configuración"):
            st.session_state.pares = {p1: p2, p2: p1}
            st.success(f"Clavijero configurado: {p1} ↔ {p2}")

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.header("Cifrar")
            txt = st.text_input("Texto original:")
            if st.button("Ejecutar Cifrado"):
                if txt: st.code(procesar_total(txt, "cifrar", st.session_state.pares))
        with col2:
            st.header("Descifrar")
            code = st.text_input("Código a descifrar:")
            if st.button("Ejecutar Descifrado"):
                if code: st.code(procesar_total(code, "descifrar", st.session_state.pares))

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
