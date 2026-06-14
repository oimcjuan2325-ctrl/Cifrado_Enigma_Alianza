import streamlit as st
import datetime

# --- CONFIGURACIÓN ---
USUARIOS_VALIDOS = {
    "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460",
    "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562",
    "Nahia": "9786", "Amets": "1053"
}

VOCALES_PAR = {'A': '22', 'E': '44', 'I': '88', 'O': '00', 'U': '11'}
VOCALES_IMPAR = {'A': '11', 'E': '22', 'I': '33', 'O': '44', 'U': '55'}
CONSONANTES = "BCDFGHJKLMNPQRSTVWXYZÑ"

# --- LÓGICA DE CIFRADO CON NÚMEROS ---
def procesar(texto, mes, dia, es_par, cifrar=True):
    res = ""
    desp = (mes + dia + 11) // 2 if es_par else (mes + dia + 12) // 2
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    inv_vocales = {v: k for k, v in vocales.items()}
    
    i = 0
    t = texto.upper()
    while i < len(t):
        # Si es vocal cifrada (2 dígitos)
        if i + 1 < len(t) and ( (cifrar and t[i] in "AEIOU") or (not cifrar and t[i:i+2] in inv_vocales) ):
            if cifrar:
                res += vocales[t[i]]
                i += 1
            else:
                res += inv_vocales[t[i:i+2]]
                i += 2
        # Si es consonante
        elif t[i] in CONSONANTES:
            idx = CONSONANTES.index(t[i])
            if cifrar:
                new_idx = (idx + desp) % len(CONSONANTES) if idx < 7 else (idx - desp) % len(CONSONANTES)
            else:
                new_idx = (idx - desp) % len(CONSONANTES) if idx < 7 else (idx + desp) % len(CONSONANTES)
            res += CONSONANTES[new_idx]
            i += 1
        else:
            res += t[i]
            i += 1
    return res

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Alianza")
if "auth" not in st.session_state: st.session_state.auth = False
if "historial" not in st.session_state: st.session_state.historial = []

if not st.session_state.auth:
    st.title("🛡️ Acceso Alianza")
    user = st.text_input("Usuario:")
    pwd = st.text_input("Contraseña:", type="password")
    if st.button("Entrar"):
        if user in USUARIOS_VALIDOS and USUARIOS_VALIDOS[user] == pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
else:
    st.sidebar.title(f"Operador: {st.session_state.user}")
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Historial"])
    
    if menu == "Cifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Texto:")
        if st.button("Ejecutar"):
            st.success(procesar(txt, f.month, f.day, f.day % 2 == 0, True))
            
    elif menu == "Descifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Mensaje cifrado:")
        if st.button("Ejecutar"):
            st.info(procesar(txt, f.month, f.day, f.day % 2 == 0, False))
            
    elif menu == "Historial":
        txt = st.text_input("Mensaje:")
        if st.button("Guardar"):
            st.session_state.historial.append(txt)
        st.write(st.session_state.historial)
