import streamlit as st
import numpy as np

# Configuración del abecedario
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
conv_dict = {letra: i + 1 for i, letra in enumerate(alfabeto)}
inv_conv_dict = {i + 1: letra for i, letra in enumerate(alfabeto)}

def cifrar_completo(mensaje):
    mensaje = mensaje.upper().replace(" ", "")
    n = len(mensaje)
    
    # 1. CAPA: Álgebra Lineal (Usamos una clave fija como ejemplo)
    # Puedes cambiar estos números por tu clave secreta de n elementos
    clave = [i + 2 for i in range(n)] 
    
    valor_algebraico = 0
    for i in range(n):
        letra = mensaje[i]
        valor_letra = conv_dict.get(letra, 0)
        valor_algebraico += clave[i] * valor_letra
    
    # 2. CAPA: Cifrado César dinámico
    # Desplazamos el resultado algebraico según el número de caracteres (n)
    resultado_final = valor_algebraico + n
    
    return resultado_final

# --- INTERFAZ ---
st.title("Sistema de Cifrado Pro")

if 'logueado' not in st.session_state:
    st.session_state.logueado = False

if not st.session_state.logueado:
    password = st.text_input("Introduce la contraseña:", type="password")
    if password == "MAQUINA":
        st.session_state.logueado = True
        st.rerun()
else:
    st.write("Bienvenido al sistema. Introduce tu mensaje para cifrar.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar")
        mensaje = st.text_input("Mensaje (sin espacios):")
        if st.button("Cifrar"):
            if mensaje:
                res = cifrar_completo(mensaje)
                st.success(f"Resultado final: {res}")
            
    with col2:
        st.subheader("Descifrar")
        st.write("El descifrado requiere revertir el César y la matriz algebraica.")
        
    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
