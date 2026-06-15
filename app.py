import streamlit as st
import numpy as np
import base64
import time

# --- LÓGICA DEL MOTOR DE CIFRADO (GEOMETRÍA 3D + DIFUSIÓN) ---
def obtener_matriz(fecha_str):
    # La fecha es la única semilla: asegura que el cifrado cambie cada día
    np.random.seed(int(fecha_str))
    matriz = np.random.rand(3, 3)
    # Convertimos en matriz de rotación ortogonal (estándar matemático)
    q, r = np.linalg.qr(matriz)
    return q

def procesar_mensaje(mensaje, fecha_str, modo='cifrar'):
    matriz = obtener_matriz(fecha_str)
    # Vector de estado inicial (usado para la difusión encadenada)
    estado = np.array([0.0, 0.0, 0.0])
    resultado = []
    
    if modo == 'descifrar':
        matriz = matriz.T # Inversa (transpuesta)
        datos = np.frombuffer(base64.b64decode(mensaje), dtype=np.float64).reshape(-1, 3)
    else:
        datos = np.array([[ord(c), i, 0] for i, c in enumerate(mensaje)])

    for v in datos:
        if modo == 'cifrar':
            # Rotación + Difusión encadenada
            v_rotado = np.dot(matriz, v) + estado
            estado = v_rotado
            resultado.append(v_rotado)
        else:
            # Reversión de difusión + Rotación inversa
            v_rotado = np.dot(matriz, (v - estado))
            estado = v
            resultado.append(v_rotado)
            
    if modo == 'cifrar':
        return base64.b64encode(np.array(resultado).tobytes()).decode()
    else:
        return "".join([chr(int(round(v[0]))) for v in resultado])

# --- INTERFAZ WEB (STREAMLIT) ---
st.set_page_config(page_title="Máquina Enigma", layout="wide")
st.title("Cifrado Enigma")

# Inicializar sesión
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

# Pantalla de Login con animación
if not st.session_state.autenticado:
    password = st.text_input("Introduzca la palabra secreta para acceder a la máquina:", type="password")
    if st.button("Acceder"):
        if password.upper() == "MAQUINA":
            st.write("Encendiendo rotores de la máquina enigma...")
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03) # Animación de 3 segundos
                progress_bar.progress(i + 1)
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Acceso denegado.")
else:
    st.header("Máquina Enigma del Cifrado de la Alianza")
    
    # Diseño de doble columna
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar Mensaje")
        msg_cifrar = st.text_area("Mensaje a cifrar:", height=150)
        fecha_cifrar = st.date_input("Fecha de cifrado:")
        if st.button("Cifrar ahora"):
            fecha_str = fecha_cifrar.strftime("%d%m%Y")
            try:
                res = procesar_mensaje(msg_cifrar, fecha_str, 'cifrar')
                st.text_area("Resultado cifrado:", res, height=150)
            except:
                st.error("Error al cifrar.")
            
    with col2:
        st.subheader("Descifrar Mensaje")
        msg_descifrar = st.text_area("Mensaje a descifrar:", height=150)
        fecha_descifrar = st.date_input("Fecha de creación original:")
        if st.button("Descifrar ahora"):
            fecha_str = fecha_descifrar.strftime("%d%m%Y")
            try:
                res = procesar_mensaje(msg_descifrar, fecha_str, 'descifrar')
                st.text_area("Resultado original:", res, height=150)
            except:
                st.error("Error: Verifique la fecha y el mensaje.")
