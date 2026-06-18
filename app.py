import streamlit as st

# Diccionario de conversión
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
conv = {letra: i + 1 for i, letra in enumerate(alfabeto)}
inv_conv = {i + 1: letra for i, letra in enumerate(alfabeto)}

def aplicar_cesar(valor, n, modo="cifrar"):
    if modo == "cifrar":
        return valor + n
    return valor - n

def cifrar(mensaje, clave):
    limpio = mensaje.upper().replace(" ", "")
    n = len(limpio)
    
    # Álgebra: Suma de (valor_letra * coeficiente_clave)
    # Ajustamos la clave a la longitud del mensaje
    val_algebraico = sum(conv.get(limpio[i], 0) * clave[i % len(clave)] for i in range(n))
    
    # César dinámico
    return aplicar_cesar(val_algebraico, n, "cifrar")

# --- INTERFAZ ---
st.set_page_config(page_title="Cifrado Pro", layout="centered")
st.title("🔐 Sistema de Cifrado Algebraico")

if 'logueado' not in st.session_state: st.session_state.logueado = False

if not st.session_state.logueado:
    password = st.text_input("Contraseña:", type="password")
    if password == "MAQUINA":
        st.session_state.logueado = True
        st.rerun()
else:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar")
        mensaje = st.text_input("Mensaje:")
        clave_str = st.text_input("Clave (números separados por coma, ej: 3,2,1):")
        if st.button("Cifrar"):
            try:
                clave = [int(x) for x in clave_str.split(",")]
                res = cifrar(mensaje, clave)
                st.success(f"Cifrado: {res}")
            except: st.error("Error en la clave.")

    with col2:
        st.subheader("Descifrar")
        st.info("Nota: Este sistema es de 'sentido único' por la suma algebraica. "
                "Para descifrar, el receptor debe conocer la clave secreta y la longitud.")

    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
