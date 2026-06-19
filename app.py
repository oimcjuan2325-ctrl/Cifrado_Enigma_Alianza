import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cifrado Algebraico Modular", page_icon="🔒")

# --- MOTOR DE CIFRADO ---
def procesar_algebraico(mensaje, modo='cifrar'):
    mapa = {
        'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
        'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'Ñ':15, 'O':16, 'P':17,
        'Q':18, 'R':19, 'S':20, 'T':21, 'U':22, 'V':23, 'W':24, 'X':25,
        'Y':26, 'Z':27
    }
    mapa_inverso = {v: k for k, v in mapa.items()}
    
    n = len(mensaje.replace(" ", ""))
    resultado = []
    
    for idx, char in enumerate(mensaje.upper()):
        if char == ' ':
            resultado.append(' ')
            continue
        
        vi = mapa.get(char, 0)
        if vi == 0: continue
            
        i = idx + 1
        if modo == 'cifrar':
            ci = (vi + (2 * i) + n) % 27
        else:
            ci = (vi - (2 * i) - n) % 27
            
        if ci <= 0: ci += 27
        resultado.append(mapa_inverso.get(ci, '?'))
        
    return "".join(resultado)

# --- ESTADOS ---
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'tiempo_bloqueo' not in st.session_state: st.session_state.tiempo_bloqueo = 0
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'tiempo_agotado' not in st.session_state: st.session_state.tiempo_agotado = False

# --- LÓGICA DE BLOQUEO ---
if st.session_state.bloqueado:
    tiempo_transcurrido = time.time() - st.session_state.tiempo_bloqueo
    if tiempo_transcurrido < 60:
        st.error(f"Lo sentimos, pero hemos visto que no eres apto para esta web. Por favor, espera que el contador llegue a cero: {int(60 - tiempo_transcurrido)}s")
        st.stop()
    else:
        st.session_state.bloqueado = False
        st.session_state.tiempo_agotado = True

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
    st.title("Máquina del Cifrado Algebraico Modular")
    op = st.radio("Selecciona una opción:", ["Cifrar", "Descifrar"])
    msg = st.text_input("Introduce tu mensaje:")
    
    if st.button("Ejecutar"):
        res = procesar_algebraico(msg, 'cifrar' if op == "Cifrar" else 'descifrar')
        # st.text_area incluye automáticamente el botón de copiar
        st.text_area("Resultado:", value=res, help="Copia este mensaje")
        
    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
