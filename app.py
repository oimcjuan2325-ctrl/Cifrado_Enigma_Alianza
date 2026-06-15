import streamlit as st

# --- CONFIGURACIÓN DE USUARIOS ---
USUARIO_VALIDO = {
    "CIDRADO ENIGMA": "2026"
}

# --- MOTORES DE CIFRADO ---
VOCALES_PAR = {'A': '22', 'E': '44', 'I': '88', 'O': '00', 'U': '11'}
VOCALES_IMPAR = {'A': '11', 'E': '22', 'I': '33', 'O': '44', 'U': '55'}
CONSONANTES = "BCDFGHJKLMNPQRSTVWXYZÑ"

def procesar(texto, mes, dia, es_par, cifrar=True):
    desp = (mes + dia + 12) // 2
    vocales = VOCALES_PAR if es_par else VOCALES_IMPAR
    inv_vocales = {v: k for k, v in vocales.items()}
    res = ""
    i = 0
    t = texto.upper()
    while i < len(t):
        if not cifrar and i + 1 < len(t) and t[i:i+2] in inv_vocales:
            res += inv_vocales[t[i:i+2]]; i += 2
        elif cifrar and t[i] in vocales:
            res += vocales[t[i]]; i += 1
        elif t[i] in CONSONANTES:
            idx = CONSONANTES.index(t[i])
            new_idx = (idx + desp) % len(CONSONANTES) if cifrar else (idx - desp) % len(CONSONANTES)
            res += CONSONANTES[new_idx]; i += 1
        else: res += t[i]; i += 1
    return res

# --- INTERFAZ ---
st.set_page_config(page_title="Enigma Alianza", layout="centered")

if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ Acceso al cifrado Enigma de la Alianza")
    usuario = st.text_input("Usuario:")
    password = st.text_input("PIN:", type="password")
    if st.button("Iniciar sesión"):
        if usuario in USUARIOS_VALIDOS and USUARIOS_VALIDOS[usuario] == password:
            st.session_state.auth = True
            st.session_state.user = usuario
            st.rerun()
        else:
            st.error("Credenciales incorrectas.")
else:
    st.title(f"Operador: {st.session_state.user}")
    if st.button("Cerrar sesión"):
        st.session_state.auth = False
        st.rerun()
    
    st.write("---")
    menu = st.radio("Acción:", ["Cifrar", "Descifrar"], horizontal=True)
    f = st.date_input("Fecha de referencia:")
    txt = st.text_area("Mensaje:")
    
    if st.button("Ejecutar"):
        resultado = procesar(txt, f.month, f.day, f.day % 2 == 0, menu == "Cifrar")
        st.code(resultado)
