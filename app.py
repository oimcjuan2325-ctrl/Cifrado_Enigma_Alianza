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

# --- MOTOR DE CIFRADO ---
def procesar(texto, mes, dia, es_par, cifrar=True):
    # Fórmula de desplazamiento única
    desp = (mes + dia + 12) // 2
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    inv_vocales = {v: k for k, v in vocales.items()}
    res = ""
    i = 0
    t = texto.upper()
    
    while i < len(t):
        # 1. Intentar descifrar vocal (2 dígitos)
        if not cifrar and i + 1 < len(t) and t[i:i+2] in inv_vocales:
            res += inv_vocales[t[i:i+2]]
            i += 2
        # 2. Cifrar vocal
        elif cifrar and t[i] in vocales:
            res += vocales[t[i]]
            i += 1
        # 3. Consonantes (Desplazamiento positivo)
        elif t[i] in CONSONANTES:
            idx = CONSONANTES.index(t[i])
            if cifrar:
                new_idx = (idx + desp) % len(CONSONANTES)
            else:
                new_idx = (idx - desp) % len(CONSONANTES)
            res += CONSONANTES[new_idx]
            i += 1
        else:
            res += t[i]
            i += 1
    return res

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Alianza")

if "auth" not in st.session_state: st.session_state.auth = False
if "user" not in st.session_state: st.session_state.user = None
if "historial" not in st.session_state: st.session_state.historial = []

if not st.session_state.auth:
    st.title("🛡️ Acceso Alianza")
    usuario = st.text_input("Usuario:")
    password = st.text_input("Contraseña:", type="password")
    if st.button("Iniciar sesión"):
        if usuario in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario] == password:
            st.session_state.auth = True
            st.session_state.user = usuario
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
else:
    st.sidebar.title(f"Operador: {st.session_state.user}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.auth = False
        st.session_state.user = None
        st.rerun()
    
    menu = st.sidebar.radio("Opciones", ["Cifrar", "Descifrar", "Historial"])
    
    if menu in ["Cifrar", "Descifrar"]:
        f = st.date_input("Fecha")
        txt = st.text_area("Texto:")
        if st.button("Ejecutar"):
            resultado = procesar(txt, f.month, f.day, f.day % 2 == 0, menu == "Cifrar")
            st.code(resultado)
            
    elif menu == "Historial":
        st.subheader("Historial de mensajes")
        txt = st.text_input("Guardar mensaje (cifrado):")
        if st.button("Guardar"):
            st.session_state.historial.append(f"{datetime.date.today()} - {txt}")
            st.success("Guardado.")
        st.write(st.session_state.historial)
