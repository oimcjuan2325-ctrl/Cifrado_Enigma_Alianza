import streamlit as st

# Configuración
st.set_page_config(page_title="Sistema de Cifrado Pro", layout="wide")

ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
CONV = {letra: i + 1 for i, letra in enumerate(ALFABETO)}

def validar_solo_letras(texto):
    # Comprueba si el texto contiene números
    if any(char.isdigit() for char in texto):
        return False
    return True

def cifrar_frase(texto, clave):
    palabras = texto.upper().split()
    resultados = []
    for palabra in palabras:
        n = len(palabra)
        valor_alg = sum(CONV.get(palabra[i], 0) * clave[i % len(clave)] for i in range(n))
        resultados.append(str(valor_alg + n))
    return " ".join(resultados)

# --- INTERFAZ ---
st.title("🔐 Sistema de Cifrado Pro")

if 'logueado' not in st.session_state: st.session_state.logueado = False

if not st.session_state.logueado:
    if st.text_input("Contraseña:", type="password") == "MAQUINA":
        st.session_state.logueado = True
        st.rerun()
else:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cifrar")
        msg = st.text_input("Mensaje a cifrar:")
        clave_input = st.text_input("Clave (ej: 3,2,1):")
        
        if st.button("Cifrar"):
            # Validación estricta
            if not validar_solo_letras(msg):
                st.error("Lo siento, pero esta web no puede procesar números para los cálculos. Por favor, escríbelos manualmente a base de letras.")
            else:
                try:
                    clave = [int(x) for x in clave_input.split(",")]
                    st.code(cifrar_frase(msg, clave))
                except:
                    st.error("Error en el formato de la clave.")

    with col2:
        st.subheader("Descifrar")
        cif_input = st.text_input("Texto cifrado:")
        if st.button("Descifrar"):
            # Validación estricta
            if not validar_solo_letras(cif_input.replace(" ", "")):
                st.info("Descifrando bloque...")
                # Aquí iría tu lógica inversa
            else:
                st.error("Lo siento, pero esta web no puede procesar letras para el descifrado. Por favor, introduce solo el código numérico.")

    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
