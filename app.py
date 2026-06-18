import streamlit as st
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema de Cifrado Modular", page_icon="🔒")

# --- MOTOR DE CIFRADO ---
def procesar_texto(mensaje, modo='cifrar'):
    n = len(mensaje)
    resultado = []
    
    for idx, char in enumerate(mensaje):
        # Si es un espacio, lo mantenemos intacto
        if char == ' ':
            resultado.append(' ')
            continue
        
        # Valor original (A=1, B=2...)
        vi = ord(char.upper()) - 64
        i = idx + 1 # Posición 1-basada
        
        # Cálculo de la capa aritmética
        if modo == 'cifrar':
            ci = (vi + (2 * i) + (2 * n)) % 27
        else: # modo descifrar
            ci = (vi - (2 * i) - (2 * n)) % 27
            
        # Ajuste de rango para que siempre sea 1-27
        if ci <= 0: ci += 27
        resultado.append(chr(ci + 64))
        
    return "".join(resultado)

# --- ESTADOS DE SESIÓN ---
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

# --- INTERFAZ ---
if not st.session_state.autenticado:
    st.title("Inicio de sesión en el cifrado de aritmética modular")
    
    if st.session_state.bloqueado:
        st.error("Lo sentimos, pero hemos visto que no eres apto para esta web.")
    else:
        password = st.text_input("Inicie sesión:", type="password")
        if st.button("Acceder"):
            if password == "MAQUINA":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.session_state.intentos += 1
                if st.session_state.intentos >= 3:
                    st.session_state.bloqueado = True
                st.warning(f"Contraseña incorrecta. Intento {st.session_state.intentos}/3")
else:
    # --- PANTALLA PRINCIPAL DENTRO ---
    st.title("Máquina del cifrado del cifrado aritmético modular")
    
    opcion = st.radio("Selecciona una operación:", ["Cifrar", "Descifrar"])
    mensaje = st.text_input("Introduce tu mensaje:")
    
    if st.button("Ejecutar Operación"):
        if mensaje:
            res = procesar_texto(mensaje, 'cifrar' if opcion == "Cifrar" else 'descifrar')
            st.success("Operación completada con éxito:")
            st.text_area("Resultado:", value=res, help="Puedes copiar este texto")
        else:
            st.error("El mensaje no puede estar vacío.")
    
    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
