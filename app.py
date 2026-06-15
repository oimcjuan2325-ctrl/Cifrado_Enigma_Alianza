import streamlit as st
import numpy as np
import base64
import time

# --- LÓGICA DEL MOTOR DE CIFRADO ---
def obtener_matriz(fecha_str):
    np.random.seed(int(fecha_str))
    matriz = np.random.rand(3, 3)
    q, r = np.linalg.qr(matriz)
    return q

def procesar_mensaje(mensaje, fecha_str, modo='cifrar'):
    matriz = obtener_matriz(fecha_str)
    estado = np.array([0.0, 0.0, 0.0])
    resultado = []
    
    if modo == 'descifrar':
        matriz = matriz.T
        datos = np.frombuffer(base64.b64decode(mensaje), dtype=np.float64).reshape(-1, 3)
    else:
        datos = np.array([[ord(c), i, 0] for i, c in enumerate(mensaje)])

    for v in datos:
        if modo == 'cifrar':
            v_rotado = np.dot(matriz, v) + estado
            estado = v_rotado
            resultado.append(v_rotado)
        else:
            v_rotado = np.dot(matriz, (v - estado))
            estado = v
            resultado.append(v_rotado)
            
    if modo == 'cifrar':
        return base64.b64encode(np.array(resultado).tobytes()).decode()
    else:
        return "".join([chr(int(round(v[0]))) for v in resultado])

# --- INTERFAZ WEB ---
st.title("Cifrado Enigma")

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    password = st.text_input("Introduzca la palabra secreta:", type="password")
    if st.button("Acceder"):
        if password.upper() == "MAQUINA":
            # Animación de 3 segundos
            st.write("Encendiendo rotores de la máquina enigma...")
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.03) # Total 3 segundos aprox
                progress_bar.progress(i + 1)
            
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Acceso denegado.")
else:
    st.header("Máquina Enigma del Cifrado de la Alianza")
    opcion = st.radio("Seleccione acción:", ["Cifrar mensaje", "Descifrar mensaje"])
    msg = st.text_area("Mensaje:")
    fecha = st.date_input("Fecha de referencia:")
    
    if st.button("Ejecutar"):
        fecha_str = fecha.strftime("%d%m%Y")
        try:
            res = procesar_mensaje(msg, fecha_str, 'cifrar' if opcion == "Cifrar mensaje" else 'descifrar')
            st.text_area("Resultado:", res, height=200)
        except Exception:
            st.error("Error: Verifique la fecha y el contenido.")
