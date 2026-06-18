import streamlit as st
from logica_enigma import cifrar_hill, aplicar_cesar_y_metadato

# Configuración estética
st.set_page_config(page_title="Cifrado Enigma", layout="wide", initial_sidebar_state="collapsed")

# Gestión de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- PANTALLA DE ACCESO ---
    st.title("🔐 Acceso a Enigma")
    st.markdown("---")
    
    # Campo de contraseña
    pwd = st.text_input("Introduce la palabra clave para entrar:", type="password")
    
    # NUEVO: Botón de iniciar sesión solicitado
    if st.button("Iniciar sesión"):
        if pwd == "máquina":
            st.session_state.logged_in = True
            st.success("Acceso concedido. Cargando sistema...")
            st.rerun()
        else:
            st.error("Palabra clave incorrecta. Inténtalo de nuevo.")

else:
    # --- PANEL DE CONTROL ---
    st.title("🛡️ Sistema de Cifrado Enigma")
    st.markdown("Bienvenido al terminal seguro. Selecciona una operación abajo.")
    st.write("")

    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📤 Cifrar Mensaje")
        txt = st.text_input("Texto original:", placeholder="Ej: HOLA")
        
        if st.button("Ejecutar Cifrado"):
            if txt:
                # 1. Proceso de Hill
                hill_res = cifrar_hill(txt)
                # 2. Capa César y Metadatos
                final, val, letra = aplicar_cesar_y_metadato(hill_res)
                
                st.info("Mensaje cifrado con éxito:")
                if val:
                    # Formato matemático profesional solicitado
                    st.latex(rf"{final}^{{+{val}{letra}}}")
                else:
                    st.success(f"### {final}")
            else:
                st.warning("Escribe algo para cifrar.")

    with col2:
        st.header("📥 Descifrar Mensaje")
        code = st.text_input("Introduce el código cifrado:", placeholder="Ej: GCAF")
        if st.button("Ejecutar Descifrado"):
            st.info("Módulo de descifrado en mantenimiento.")

    # Botón de salida
    st.sidebar.markdown("---")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()
