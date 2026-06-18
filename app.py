import streamlit as st
import time
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Sistema de Cifrado")

# --- FUNCIONES DE CIFRADO/DESCIFRADO ---
def cifrar(mensaje):
    n = len(mensaje)
    # Convertimos a valores (A=1, B=2...) y aplicamos fórmula con NumPy
    vals = np.array([ord(c.upper()) - 64 for c in mensaje])
    i = np.arange(1, n + 1)
    res = (vals + (2 * i) + (2 * n)) % 27
    res[res == 0] = 27 # Ajuste para que Z=27
    return "".join([chr(v + 64) for v in res])

def descifrar(mensaje):
    n = len(mensaje)
    # Proceso inverso: restamos lo que antes sumamos
    vals = np.array([ord(c.upper()) - 64 for c in mensaje])
    i = np.arange(1, n + 1)
    res = (vals - (2 * i) - (2 * n)) % 27
    res[res <= 0] += 27 # Ajuste para volver al rango positivo
    return "".join([chr(v + 64) for v in res])

# --- ESTADOS ---
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'tiempo_bloqueo' not in st.session_state: st.session_state.tiempo_bloqueo = 0
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tiempo_agotado' not in st.session_state: st.session_state.tiempo_agotado = False

# --- LOGICA DE BLOQUEO ---
if st.session_state.bloqueado:
    tiempo_transcurrido = time.time() - st.session_state.tiempo_bloqueo
    if tiempo_transcurrido < 60:
        st.error(f"Lo sentimos, pero hemos visto que no eres apto para esta web. Por favor, espera a que el contador llegue a cero: {int(60 - tiempo_transcurrido)}s")
        st.stop()
    else:
        st.session_state.bloqueado = False
        st.session_state.tiempo_agotado = True
        st.session_state.intentos = 0

# --- INTERFAZ ---
if not st.session_state.autenticado:
    st.title("Inicio de sesión en el cifrado de aritmética modular")
    if st.session_state.tiempo_agotado:
        st.warning("Lo sentimos, aunque haya acabado el contador, no puede iniciar sesión.")
    password = st.text_input("Inicie sesión:", type="password")
    if st.button("Acceder"):
        if password == "MAQUINA":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.session_state.intentos += 1
            if st.session_state.intentos >= 3:
                st.session_state.bloqueado = True
                st.session_state.tiempo_bloqueo = time.time()
            st.warning(f"Contraseña incorrecta. Intento {st.session_state.intentos}/3")
else:
    st.title("Máquina del cifrado del cifrado aritmético modular")
    opcion = st.radio("Selecciona una opción:", ["Cifrar", "Descifrar"])
    mensaje = st.text_input("Introduce tu mensaje:")
    if st.button("Ejecutar"):
        if opcion == "Cifrar":
            res = cifrar(mensaje)
        else:
            res = descifrar(mensaje)
        st.text_area("Resultado:", value=res, help="Puedes copiar este texto")
    
    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
