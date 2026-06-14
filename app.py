import streamlit as st
import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
USUARIOS_VALIDOS = {
    "Juan": "2313", "Asier": "2021", "Jesús": "1365", "Yolanda": "1460",
    "Mikel": "2013", "Gaizka": "9837", "Iñaki": "7467", "Erika": "7562",
    "Nahia": "9786", "Amets": "1053"
}

# --- LÓGICA DE CIFRADO ---
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
if "user" not in st.session_state: st.session_state.user = None
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
        else:
            st.error("Credenciales incorrectas.")
else:
    st.sidebar.title(f"Operador: {st.session_state.user}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.auth = False
        st.rerun()
        
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Guardar en Historial"])
    
    if menu == "Cifrar":
        st.subheader("Cifrar mensaje")
        f = st.date_input("Fecha")
        txt = st.text_area("Texto a cifrar:")
        if st.button("Ejecutar"):
            res = procesar(txt, f.month, f.day, f.day % 2 == 0, True)
            st.code(res)
            
    elif menu == "Descifrar":
        st.subheader("Descifrar mensaje")
        f = st.date_input("Fecha de cifrado")
        txt = st.text_area("Mensaje cifrado:")
        if st.button("Ejecutar"):
            res = procesar(txt, f.month, f.day, f.day % 2 == 0, False)
            st.code(res)
            
    elif menu == "Guardar en Historial":
        st.subheader("Registro de mensajes")
        f = st.date_input("Fecha del cifrado")
        txt = st.text_input("Mensaje cifrado:")
        if st.button("Guardar"):
            st.session_state.historial.append({"Fecha": str(f), "Mensaje": txt})
            st.success("Guardado correctamente.")
        st.table(st.session_state.historial)
