import streamlit as st
from logica_enigma import cifrar_hill, aplicar_cesar_y_metadato

st.set_page_config(page_title="Cifrado Enigma", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Acceso a Enigma")
    pwd = st.text_input("Palabra clave:", type="password")
    if pwd == "máquina":
        st.session_state.logged_in = True
        st.rerun()
else:
    st.title("🔐 Sistema Cifrado Enigma")
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Cifrar")
        txt = st.text_input("Introduce texto para cifrar:")
        if st.button("Cifrar"):
            hill = cifrar_hill(txt)
            final, val, letra = aplicar_cesar_y_metadato(hill)
            if val:
                st.subheader("Resultado:")
                st.latex(rf"{final}^{{+{val}{letra}}}")
            else:
                st.subheader("Resultado:")
                st.write(f"### {final}")

    with col2:
        st.header("Descifrar")
        code = st.text_input("Introduce código (ej: GCAF):")
        if st.button("Descifrar"):
            st.info("Función de descifrado lista para implementar.")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
