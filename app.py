import streamlit as st
import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
USUARIOS_VALIDOS = {
    "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460",
    "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562",
    "Nahia": "9786", "Amets": "1053"
}

VOCALES_PAR = {'A': '22', 'E': '44', 'I': '88', 'O': '00', 'U': '11'}
VOCALES_IMPAR = {'A': '11', 'E': '22', 'I': '33', 'O': '44', 'U': '55'}
CONSONANTES = "BCDFGHJKLMNPQRSTVWXYZÑ"

# --- MOTOR DE CIFRADO ---
def procesar(texto, mes, dia, es_par, cifrar=True):
    desp = (mes + dia + 11) // 2 if es_par else (mes + dia + 12) // 2
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    inv_vocales = {v: k for k, v in vocales.items()}
    res = ""
    
    i = 0
    t = texto.upper()
    while i < len(t):
        # 1. ¿Es vocal cifrada (2 números)?
        if not cifrar and i + 1 < len(t) and t[i:i+2] in inv_vocales:
            res += inv_vocales[t[i:i+2]]
            i += 2
        # 2. ¿Es vocal a cifrar?
        elif cifrar and t[i] in vocales:
            res += vocales[t[i]]
            i += 1
        # 3. ¿Es consonante?
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
    if st.button("Iniciar sesión"):
        if user in USUARIOS_VALIDOS and USUARIOS_VALIDOS[user] == pwd:
            st.session_state.auth = True
            st.session_state.user = user
            st.rerun()
        else: st.error("Acceso incorrecto.")
else:
    # Sidebar con botón de cerrar sesión
    st.sidebar.title(f"Operador: {st.session_state.user}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.auth = False
        st.rerun()
        
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Historial"])
    
    if menu == "Cifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Texto a cifrar:")
        if st.button("Cifrar"):
            st.success(procesar(txt, f.month, f.day, f.day % 2 == 0, True))
            
    elif menu == "Descifrar":
        f = st.date_input("Fecha")
        txt = st.text_area("Mensaje cifrado:")
        if st.button("Descifrar"):
            st.info(procesar(txt, f.month, f.day, f.day % 2 == 0, False))
            
    elif menu == "Historial":
        txt = st.text_input("Guardar mensaje (Cifrado):")
        if st.button("Guardar"):
            st.session_state.historial.append({"Fecha": str(datetime.date.today()), "Msg": txt})
        st.table(st.session_state.historial)
