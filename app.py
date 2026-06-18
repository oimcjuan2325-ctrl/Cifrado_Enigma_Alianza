import streamlit as st
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Sistema de Cifrado Modular",
    page_icon="🔒",
    layout="centered"
)

# --- LÓGICA MATEMÁTICA (MOTOR DE CIFRADO) ---
def aplicar_transformacion(mensaje, modo='cifrar'):
    """Aplica la fórmula: Ci = (Vi + 2*i + 2*n) mod 27"""
    n = len(mensaje)
    # Convertimos a valores (A=1, B=2...)
    # Usamos np.array para cálculos vectorizados rápidos
    vals = np.array([ord(c.upper()) - 64 for c in mensaje])
    i = np.arange(1, n + 1)
    
    if modo == 'cifrar':
        res = (vals + (2 * i) + (2 * n)) % 27
    else: # modo descifrar
        res = (vals - (2 * i) - (2 * n)) % 27
    
    # Ajuste de rango 1-27
    res[res <= 0] += 27
    return "".join([chr(v + 64) for v in res])

# --- GESTIÓN DE SESIÓN ---
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

# --- INTERFAZ DE USUARIO ---
def main():
    if not st.session_state.autenticado:
        st.title("Inicio de sesión en el cifrado de aritmética modular")
        
        if st.session_state.bloqueado:
            st.error("Lo sentimos, pero hemos visto que no eres apto para esta web.")
            return

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
        # PANTALLA PRINCIPAL
        st.title("Máquina del cifrado del cifrado aritmético modular")
        
        opcion = st.radio("Selecciona una operación:", ["Cifrar", "Descifrar"])
        mensaje = st.text_input("Introduce tu mensaje:")
        
        if st.button("Ejecutar Operación"):
            if mensaje:
                resultado = aplicar_transformacion(mensaje, 'cifrar' if opcion == "Cifrar" else 'descifrar')
                st.success("Operación completada con éxito:")
                st.text_area("Resultado:", value=resultado, help="Pulsa el icono de copiar a la derecha")
            else:
                st.error("El mensaje no puede estar vacío.")
        
        st.divider()
        if st.button("Cerrar sesión"):
            st.session_state.autenticado = False
            st.rerun()

if __name__ == "__main__":
    main()
