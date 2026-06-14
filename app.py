import streamlit as st
import datetime

# --- CONFIGURACIÓN DE USUARIOS ---
USUARIOS_VALIDOS = {
    "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460",
    "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562",
    "Nahia": "9786", "Amets": "1053"
}

# --- LÓGICA DE CIFRADO ---
VOCALES_PAR = {'A': '22', 'E': '44', 'I': '88', 'O': '00', 'U': '11'}
VOCALES_IMPAR = {'A': '11', 'E': '22', 'I': '33', 'O': '44', 'U': '55'}
CONSONANTES = "BCDFGHJKLMNPQRSTVWXYZÑ"

def procesar(texto, mes, dia, es_par, cifrar=True):
    res = ""
    desp = (mes + dia + 11) // 2 if es_par else (mes + dia + 12) // 2
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    inv_vocales = {v: k for k, v in vocales.items()}
    
    i = 0
    texto = texto.upper()
    while i < len(texto):
        if i + 1 < len(texto) and texto[i:i+2] in (inv_vocales.values() if cifrar else inv_vocales):
            val = texto[i:i+2]
            res += inv_vocales[val] if not cifrar else vocales[val]
            i += 2
        elif texto[i] in CONSONANTES:
            idx = CONSONANTES.index(texto[i])
            if cifrar:
                new_idx = (idx + desp) % len(CONSONANTES) if idx < 7 else (idx - desp) % len(CONSONANTES)
            else:
                new_idx = (idx - desp) % len(CONSONANTES) if idx < 7 else (idx + desp) % len(CONSONANTES)
            res += CONSONANTES[new_idx]
            i += 1
        else:
            res += texto[i]
            i += 1
    return res

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Alianza", layout="centered")

if "auth" not in st.session_state: st.session_state.auth = False
if "historial" not in st.session_state: st.session_state.historial = []

if not st.session_state.auth:
    st.title("🛡️ Acceso Alianza - Project Delta")
    usuario_input = st.text_input("Nombre de cuenta:")
    pass_input = st.text_input("Contraseña:", type="password")
    if st.button("Iniciar sesión"):
        if usuario_input in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario_input] == pass_input:
            st.session_state.auth = True
            st.session_state.user = usuario_input
            st.rerun()
        else: st.error("Credenciales incorrectas.")
else:
    st.sidebar.title(f"Operador: {st.session_state.user}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.auth = False
        st.rerun()
    
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Historial"])
    
    if menu == "Cifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Texto a cifrar:")
        if st.button("Ejecutar"):
            st.code(procesar(txt, f.month, f.day, f.day % 2 == 0, True))
            
    elif menu == "Descifrar":
        f = st.date_input("Fecha de cifrado")
        txt = st.text_area("Mensaje cifrado:")
        if st.button("Ejecutar"):
            st.code(procesar(txt, f.month, f.day, f.day % 2 == 0, False))
            
    elif menu == "Historial":
        st.subheader("Registro de mensajes")
        txt = st.text_input("Mensaje cifrado a guardar:")
        if st.button("Guardar"):
            st.session_state.historial.append({"Operador": st.session_state.user, "Mensaje": txt})
        st.table(st.session_state.historial)
