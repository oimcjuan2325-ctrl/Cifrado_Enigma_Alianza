import streamlit as st

# Alfabeto base
alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
conv = {letra: i + 1 for i, letra in enumerate(alfabeto)}
inv_conv = {i + 1: letra for i, letra in enumerate(alfabeto)}

def procesar(texto, clave, modo):
    # Ignoramos espacios para el cálculo
    limpio = texto.upper().replace(" ", "")
    n = len(limpio)
    
    if modo == "cifrar":
        # Álgebra + César
        val = sum(conv.get(limpio[i], 0) * clave[i % len(clave)] for i in range(n))
        return val + n
    else:
        # Revertir César - Álgebra (descifrado simple)
        # Nota: Como es una suma, el descifrado exacto requiere tu clave de bloques
        val_sin_cesar = int(texto) - n
        return f"Procesado: {val_sin_cesar}"

st.title("🔐 Sistema de Cifrado")

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
        msg = st.text_input("Mensaje a cifrar:")
        clave_input = st.text_input("Clave (números ej: 3,2,1):")
        if st.button("Cifrar"):
            clave = [int(x) for x in clave_input.split(",")]
            st.write("Resultado:", procesar(msg, clave, "cifrar"))

    with col2:
        st.subheader("Descifrar")
        cif_input = st.text_input("Número cifrado:")
        n_caracteres = st.number_input("Nº caracteres:", min_value=1)
        if st.button("Descifrar"):
            st.write("Resultado:", int(cif_input) - n_caracteres)

    if st.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()
