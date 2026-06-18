import streamlit as st
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Sistema de Cifrado", layout="wide")

# Abecedario definido como constante
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CONV = {letra: i + 1 for i, letra in enumerate(ALFABETO)}
INV_CONV = {i + 1: letra for i, letra in enumerate(ALFABETO)}

# --- LÓGICA CORE ---
def transformar(texto, modo):
    """
    Aplica la fórmula: (Valor + Posición + Longitud) % 27
    """
    texto = texto.upper().replace(" ", "")
    if not texto: return ""
    resultado = []
    n = len(texto)
    for i, char in enumerate(texto):
        if char not in CONV: continue
        valor_letra = CONV[char]
        
        if modo == "cifrar":
            nuevo_val = (valor_letra + (i + 1) + n) % 27
        else:
            nuevo_val = (valor_letra - (i + 1) - n) % 27
            
        idx = nuevo_val if nuevo_val != 0 else 27
        resultado.append(INV_CONV[idx])
    return "".join(resultado)

# --- GESTIÓN DE ESTADO ---
if 'logueado' not in st.session_state: st.session_state.logueado = False
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False

# --- INTERFAZ ---
st.title("🔐 Sistema de Cifrado")

# Bloqueo por seguridad
if st.session_state.bloqueado:
    st.error("⚠️ Acceso denegado por seguridad.")
    placeholder = st.empty()
    for i in range(60, 0, -1):
        placeholder.metric("Tiempo de espera:", f"{i} seg")
        time.sleep(1)
    st.session_state.bloqueado = False
    st.session_state.intentos = 0
    st.rerun()

# Login
if not st.session_state.logueado:
    password = st.text_input("Introduce la contraseña:", type="password")
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
    # Interfaz principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar")
        msg = st.text_input("Mensaje a cifrar:", key="c1")
        if st.button("Ejecutar Cifrado"):
            res = transformar(msg, 'cifrar')
            st.code(res) # Permite copiar fácilmente
            
    with col2:
        st.subheader("Descifrar")
        cif = st.text_input("Mensaje cifrado:", key="c2")
        if st.button("Ejecutar Descifrar"):
            res = transformar(cif, 'descifrar')
            st.code(res)
    
    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
