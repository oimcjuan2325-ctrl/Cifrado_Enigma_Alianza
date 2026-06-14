import streamlit as st
import datetime

# --- LÓGICA DEL CIFRADO (Codex Delta/Enigma) ---
VOCALES_PAR = {'A': '22', 'E': '44', 'I': '88', 'O': '00', 'U': '11'}
VOCALES_IMPAR = {'A': '11', 'E': '22', 'I': '33', 'O': '44', 'U': '55'}
CONSONANTES = "BCDFGHJKLMNPQRSTVWXYZÑ"

def obtener_desplazamiento(mes, dia, es_par):
    return (mes + dia + 11) // 2 if es_par else (mes + dia + 12) // 2

def procesar(texto, mes, dia, es_par, cifrar=True):
    res = ""
    desp = obtener_desplazamiento(mes, dia, es_par)
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    for char in texto.upper():
        if char in vocales:
            res += vocales[char]
        elif char in CONSONANTES:
            idx = CONSONANTES.index(char)
            # Regla: Grupo 1 (0-6) suma, Grupo 2 (7+) resta
            if cifrar:
                new_idx = (idx + desp) % len(CONSONANTES) if idx < 7 else (idx - desp) % len(CONSONANTES)
            else:
                new_idx = (idx - desp) % len(CONSONANTES) if idx < 7 else (idx + desp) % len(CONSONANTES)
            res += CONSONANTES[new_idx]
        else:
            res += char
    return res

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Alianza", layout="centered")

if "auth" not in st.session_state: st.session_state.auth = False
if "historial" not in st.session_state: st.session_state.historial = []

if not st.session_state.auth:
    st.title("🛡️ Iniciar Sesión - Enigma")
    user = st.text_input("Nombre de cuenta:")
    password = st.text_input("Palabra secreta:", type="password")
    if st.button("Entrar"):
        if password == "CIFRADO ENIGMA":
            st.session_state.auth = True
            st.rerun()
        else: st.error("Acceso denegado.")
else:
    st.sidebar.title("Menú")
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Historial"])
    
    if menu == "Cifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Texto a cifrar:")
        if st.button("Cifrar"):
            res = procesar(txt, f.month, f.day, f.day % 2 == 0, True)
            st.success(f"Resultado: {res}")
            
    elif menu == "Descifrar":
        f = st.date_input("Fecha de cifrado")
        txt = st.text_area("Mensaje cifrado:")
        if st.button("Descifrar"):
            res = procesar(txt, f.month, f.day, f.day % 2 == 0, False)
            st.info(f"Mensaje original: {res}")
            
    elif menu == "Historial":
        f = st.date_input("Fecha del mensaje a guardar")
        txt = st.text_input("Mensaje cifrado:")
        if st.button("Guardar en Historial"):
            st.session_state.historial.append({"fecha": str(f), "msg": txt})
        st.table(st.session_state.historial)
