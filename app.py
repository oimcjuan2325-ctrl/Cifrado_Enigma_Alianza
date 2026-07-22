import streamlit as st
import numpy as np
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cifrado Trigonométrico + Binario", page_icon="🔒", layout="wide")

# --- ESTILOS CSS MATRIX / HACKER ---
st.markdown("""
<style>
    .matrix-box {
        background-color: #0d0d0d;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00ff41;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        text-align: center;
        margin-top: 10px;
    }
    .matrix-text {
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    .matrix-rain {
        color: #008011;
        font-size: 13px;
        opacity: 0.8;
    }
    /* Estilizado del bloque de código para alinearse con el diseño Matrix */
    div[data-baseweb="code-block"] {
        border: 1px solid #00ff41 !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE CIFRADO TRIGONOMÉTRICO Y BINARIO ---
MAPA = {
    'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
    'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'Ñ':15, 'O':16, 'P':17,
    'Q':18, 'R':19, 'S':20, 'T':21, 'U':22, 'V':23, 'W':24, 'X':25,
    'Y':26, 'Z':27
}
MAPA_INVERSO = {v: k for k, v in MAPA.items()}

def calcular_desplazador(vi, operacion):
    angulo_rad = np.radians(vi)
    if operacion == 'SEN':
        val = np.sin(angulo_rad)
    elif operacion == 'COS':
        val = np.cos(angulo_rad)
    else:  # TAN
        val = np.tan(angulo_rad)
        
    desplazamiento = int(np.round(val * 10))
    if desplazamiento == 0:
        desplazamiento = 1
    return desplazamiento

def obtener_operacion(idx_letra):
    operaciones = ['SEN', 'COS', 'TAN']
    return operaciones[idx_letra % 3]

def texto_a_binario(texto):
    """Convierte texto plano en cadena binaria de 8 bits"""
    return " ".join(format(ord(c), '08b') for c in texto)

def binario_a_texto(cadena_binaria):
    """Convierte cadena binaria de 8 bits separada por espacios de vuelta a texto"""
    try:
        bytes_lista = cadena_binaria.strip().split()
        return "".join(chr(int(b, 2)) for b in bytes_lista)
    except:
        return cadena_binaria

def procesar_trigonometrico_paso_a_paso(mensaje, modo='cifrar'):
    pasos = []
    resultado = []
    idx_letra = 0
    
    mensaje_procesar = mensaje
    if modo == 'descifrar' and all(c in '01 ' for c in mensaje.strip()):
        mensaje_procesar = binario_a_texto(mensaje)

    for idx_char, char in enumerate(mensaje_procesar.upper()):
        if char in [' ', 'Á', 'É', 'Í', 'Ó', 'Ú']:
            remplazos = {'Á':'A', 'É':'E', 'Í':'I', 'Ó':'O', 'Ú':'U'}
            char = remplazos.get(char, char)

        if char == ' ':
            resultado.append(' ')
            continue
            
        vi = MAPA.get(char, 0)
        if vi == 0:
            resultado.append(char)
            continue
            
        x = idx_letra + 1
        operacion = obtener_operacion(idx_letra)
        
        if modo == 'cifrar':
            shift = calcular_desplazador(vi, operacion)
            ci = (vi + shift) % 27
            if ci == 0: ci = 27
            char_res = MAPA_INVERSO.get(ci, '?')
            val_origen = vi
            val_final = ci
        else:
            ci = vi
            val_origen = ci
            char_res = '?'
            shift = 0
            val_final = 0
            
            for cand in range(1, 28):
                s_cand = calcular_desplazador(cand, operacion)
                if (cand + s_cand - 1) % 27 + 1 == ci:
                    val_final = cand
                    char_res = MAPA_INVERSO.get(cand, '?')
                    shift = s_cand
                    break

        resultado.append(char_res)
        
        pasos.append({
            'posicion': x,
            'original': char,
            'valor_original': val_origen,
            'operacion': operacion,
            'desplazamiento': shift,
            'resultado_num': val_final if modo == 'descifrar' else ci,
            'resultado_char': char_res
        })
        idx_letra += 1
        
    texto_trig_res = "".join(resultado)
    return texto_trig_res, pasos

# --- ESTADOS ---
if 'intentos' not in st.session_state: st.session_state.intentos = 0
if 'bloqueado' not in st.session_state: st.session_state.bloqueado = False
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

# --- INTERFAZ ---
if not st.session_state.autenticado:
    st.title("Inicio de sesión en el cifrado trigonométrico")
    
    if st.session_state.bloqueado:
        st.error("Lo sentimos, pero no tiene acceso a esta web.")
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
    st.title("Máquina de Cifrado Trigonométrico + Transmisión Binaria")
    
    col_izquierda, col_derecha = st.columns([1, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Controles")
        op = st.radio("Selecciona una opción:", ["Cifrar", "Descifrar"])
        msg = st.text_input("Introduce tu mensaje (Texto o Binario):")
        btn_ejecutar = st.button("Ejecutar")

    with col_derecha:
        st.subheader("🎬 Simulación del proceso")
        pantalla_simulacion = st.empty()
        pantalla_simulacion.info("Introduce un mensaje y pulsa 'Ejecutar' para ver la simulación en directo.")

    if btn_ejecutar:
        if not msg.strip():
            st.warning("Por favor, introduce un texto válido.")
        else:
            modo = 'cifrar' if op == "Cifrar" else 'descifrar'
            res_trig, pasos = procesar_trigonometrico_paso_a_paso(msg, modo)
            
            num_pasos = len(pasos) + 1
            tiempo_espera = max(1.2, 12.0 / num_pasos)
            
            progreso_bar = col_derecha.progress(0)
            
            # 1. Pasos paso a paso
            for i, paso in enumerate(pasos):
                progreso_bar.progress((i + 1) / num_pasos)
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {i+1} de {num_pasos} — Cifrado Trigonométrico: **'{paso['original']}'**")
                    
                    if modo == 'cifrar':
                        st.metric("Letra entrada", f"{paso['original']} (Valor: {paso['valor_original']})")
                        st.write(f"**Función:** `{paso['operacion']}({paso['valor_original']}°)` | **Desplazamiento:** `+{paso['desplazamiento']}`")
                        st.latex(
                            rf"({paso['valor_original']} + \text{{{paso['operacion']}}}({paso['valor_original']}^\circ)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                        )
                    else:
                        st.metric("Letra cifrada recibida", f"{paso['original']} (Valor: {paso['valor_original']})")
                        st.write(f"**Búsqueda inversa con:** `{paso['operacion']}` | **Desplazamiento detectado:** `-{paso['desplazamiento']}`")
                        st.latex(
                            rf"({paso['valor_original']} - \text{{{paso['operacion']}}}(\text{{origen}}^\circ)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                        )
                
                time.sleep(tiempo_espera)
                
            # 2. Paso Final con el Botón de Copiar Integrado en la Zona Subrayada
            progreso_bar.progress(1.0)
            
            if modo == 'cifrar':
                res_binario = texto_a_binario(res_trig)
                res_final_output = res_binario
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {num_pasos} de {num_pasos} — ⚡ Conversión a Código Binario (Matrix)")
                    
                    st.markdown(f"""
                    <div class="matrix-box">
                        <div class="matrix-rain">01100101 01110011 01110100 01101111 00100000 01100101 01110011 00100000 01110101 01101110 00100000 01101101 01100101 01101110 01110011 01100001 01101010 01100011 01101011 01100101 01110011</div>
                        <br>
                        <div>TEXTO CIFRADO: <span style="color:#ffffff;">{res_trig}</span></div>
                        <br>
                        <div class="matrix-text">⚡ BINARIO TRANSMITIDO ⚡</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # AQUÍ ESTÁ EL BLOQUE SUBRAYADO CON BOTÓN DE COPIAR INTEGRADO (Símbolo de copiar arriba a la derecha)
                    st.code(res_binario, language="text")
            else:
                res_final_output = res_trig
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {num_pasos} de {num_pasos} — 🔓 Decodificación de Pulsos Binarios Completa")
                    st.markdown(f"""
                    <div class="matrix-box">
                        <div class="matrix-text">MENSAJE DESCIFRADO CON ÉXITO</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(res_trig, language="text")
            
            time.sleep(2.0)
            col_derecha.success("¡Proceso completado!")
            
            st.divider()
            st.subheader("📌 Resultado Final")
            st.text_area("Mensaje listo para copiar o enviar:", value=res_final_output, help="Copia este mensaje")

    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
