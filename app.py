import streamlit as st
import numpy as np
import pandas as pd
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cifrado Trigonométrico 2D", page_icon="🔒", layout="wide")

# --- MOTOR DE CIFRADO Y DESCIFRADO TRIGONOMÉTRICO ---
MAPA = {
    'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8, 'I':9,
    'J':10, 'K':11, 'L':12, 'M':13, 'N':14, 'Ñ':15, 'O':16, 'P':17,
    'Q':18, 'R':19, 'S':20, 'T':21, 'U':22, 'V':23, 'W':24, 'X':25,
    'Y':26, 'Z':27
}
MAPA_INVERSO = {v: k for k, v in MAPA.items()}

def calcular_desplazador(x, vi, operacion):
    angulo = ((x * 15 + vi * 5) % 80 + 5) * (np.pi / 180)
    if operacion == 'SEN':
        val = np.sin(angulo)
    elif operacion == 'COS':
        val = np.cos(angulo)
    else:  # TAN
        val = np.tan(angulo)
        
    desplazamiento = int(np.round(val * 10))
    if desplazamiento == 0:
        desplazamiento = 1
    return desplazamiento, angulo

def obtener_operacion(idx_letra):
    operaciones = ['SEN', 'COS', 'TAN']
    return operaciones[idx_letra % 3]

def procesar_trigonometrico_paso_a_paso(mensaje, modo='cifrar'):
    pasos = []
    resultado = []
    idx_letra = 0
    
    for idx_char, char in enumerate(mensaje.upper()):
        if char == ' ':
            resultado.append(' ')
            continue
            
        vi = MAPA.get(char, 0)
        if vi == 0:
            resultado.append(char)
            continue
            
        x = idx_letra + 1
        operacion = obtener_operacion(idx_letra)
        shift, angulo = calcular_desplazador(x, vi, operacion)
        
        if modo == 'cifrar':
            ci = (vi + shift) % 27
            if ci <= 0: ci += 27
        else:
            ci = (vi - shift) % 27
            if ci <= 0: ci += 27
            
        char_res = MAPA_INVERSO.get(ci, '?')
        resultado.append(char_res)
        
        pasos.append({
            'posicion': x,
            'original': char,
            'valor_original': vi,
            'operacion': operacion,
            'angulo_deg': np.degrees(angulo),
            'desplazamiento': shift,
            'resultado_num': ci,
            'resultado_char': char_res
        })
        idx_letra += 1
        
    return "".join(resultado), pasos

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
    st.title("Máquina del Cifrado Trigonométrico 2D")
    
    col_izquierda, col_derecha = st.columns([1, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Controles")
        op = st.radio("Selecciona una opción:", ["Cifrar", "Descifrar"])
        msg = st.text_input("Introduce tu mensaje:")
        btn_ejecutar = st.button("Ejecutar")

    with col_derecha:
        st.subheader("🎬 Simulación visual del proceso")
        pantalla_simulacion = st.empty()
        pantalla_simulacion.info("Introduce un mensaje y pulsa 'Ejecutar' para ver los cálculos en el plano 2D.")

    if btn_ejecutar:
        if not msg.strip():
            st.warning("Por favor, introduce un texto válido.")
        else:
            modo = 'cifrar' if op == "Cifrar" else 'descifrar'
            res_final, pasos = procesar_trigonometrico_paso_a_paso(msg, modo)
            
            num_pasos = len(pasos)
            tiempo_espera = max(1.5, 15.0 / num_pasos if num_pasos > 0 else 2.0)
            
            progreso_bar = col_derecha.progress(0)
            
            for i, paso in enumerate(pasos):
                progreso_bar.progress((i + 1) / num_pasos)
                
                # Datos para el gráfico nativo de Streamlit
                df_puntos = pd.DataFrame({
                    'Eje X (Posición)': [paso['posicion'], paso['posicion']],
                    'Eje Y (Valor Alfabético)': [paso['valor_original'], paso['resultado_num']],
                    'Estado': [f"Original '{paso['original']}'", f"Resultado '{paso['resultado_char']}'"]
                })
                
                with pantalla_simulacion.container():
                    st.markdown(f"#### Paso {i+1} de {num_pasos} — Letra: **'{paso['original']}'**")
                    
                    # Gráfico cartesiano mediante Streamlit Scatter Chart
                    st.scatter_chart(
                        df_puntos,
                        x='Eje X (Posición)',
                        y='Eje Y (Valor Alfabético)',
                        color='Estado',
                        size=200
                    )
                    
                    st.write(f"**Función:** `{paso['operacion']}` | **Ángulo:** `{paso['angulo_deg']:.1f}°` | **Desplazamiento:** `{'+' if modo == 'cifrar' else '-'}{paso['desplazamiento']}`")
                    st.latex(
                        rf"({paso['valor_original']} {'+' if modo == 'cifrar' else '-'} \text{{{paso['operacion']}}}(\theta)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                    )
                
                time.sleep(tiempo_espera)
                
            col_derecha.success("¡Proceso completado!")
            
            st.divider()
            st.subheader("📌 Resultado Final")
            st.text_area("Mensaje obtenido:", value=res_final, help="Copia este mensaje")

    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
