import streamlit as st
from logica_enigma import cifrar_hill, descifrar_hill

st.set_page_config(page_title="Cifrado Enigma", layout="wide")

if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acceso a Enigma")
    pwd = st.text_input("Palabra clave:", type="password")
    if st.button("Iniciar sesión"):
        if pwd == "máquina":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
else:
    st.title("🛡️ Sistema Cifrado Enigma")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Cifrar")
        txt = st.text_input("Texto original:")
        if st.button("Cifrar"):
            st.success(f"Resultado: {cifrar_hill(txt)}")

    with col2:
        st.header("Descifrar")
        code = st.text_input("Código a descifrar:")
        if st.button("Descifrar"):
            st.info(f"Mensaje original: {descifrar_hill(code)}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
