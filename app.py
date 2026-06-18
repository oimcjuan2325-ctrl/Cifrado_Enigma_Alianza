import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema de Cifrado", layout="wide")

# Abecedario definido como constante
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CONV = {letra: i + 1 for i, letra in enumerate(ALFABETO)}
INV_CONV = {i + 1: letra for i, letra in enumerate(ALFABETO)}

# --- LÓGICA CORE (ROBUSTA) ---
def transformar(texto, modo):
    """
    Transforma el texto usando la lógica de desplazamiento variable:
    (Valor + Posición + Longitud) % 27
    """
    texto = texto.upper().replace(" ", "")
    if not texto:
        return ""
    
    resultado = []
    n = len(texto)
    
    try:
        for i, char in enumerate(texto):
            if char not in CONV:
                continue # Ignora caracteres fuera del abecedario definido
            
            valor_letra = CONV[char]
            
            if modo == "cifrar":
                nuevo_val = (valor_letra + (i + 1) + n) % 27
            else:
                nuevo_val = (valor_letra - (i + 1) - n) % 27
            
            # Ajuste de módulo para asegurar rango 1-27
            idx = nuevo_val if nuevo_val != 0 else 27
            resultado.append(INV_CONV[idx])
            
        return "".join(resultado)
    except Exception as e:
        return f"Error en procesamiento: {e}"

# --- GESTIÓN DE SESIÓN ---
if 'logueado' not in st.session_state: st.session_state.logueado = False
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False

# --- INTERFAZ DE USUARIO ---
st.title("🔐 Sistema de Cifrado")

# Bloqueo de seguridad
if st.session_state.bloqueado:
    st.error("⚠️ Acceso restringido por motivos de seguridad.")
    placeholder = st.empty()
    for i in range(60, 0, -1):
        placeholder.metric("Tiempo de espera para reintento:", f"{i} segundos")
        time.sleep(1)
    st.session_state.bloqueado = False
    st.session_state.intentos = 0
    st.rerun()

# Login
if not st.session_state.logueado:
    password = st.text_input("Introduce la contraseña de acceso:", type="password")
    if st.button("Acceder"):
        if password == "MAQUINA":
            st.session_state.logueado = True
            st.rerun()
        else:
            st.session_state.intentos += 1
            if st.session_state.intentos >= 3:
                st.session_state.bloqueado = True
                st.rerun()
            st.warning(f"Contraseña incorrecta. Intento {st.session_state.intentos}/3")
else:
    # Área de trabajo
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar")
        msg = st.text_input("Mensaje a cifrar:", key="cifrar_input")
        if st.button("Ejecutar Cifrado"):
            st.success(f"Resultado: {transformar(msg, 'cifrar')}")
            
    with col2:
        st.subheader("Descifrar")
        cif = st.text_input("Mensaje cifrado:", key="descifrar_input")
        if st.button("Ejecutar Descifrado"):
            st.success(f"Resultado: {transformar(cif, 'descifrar')}")
    
    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
