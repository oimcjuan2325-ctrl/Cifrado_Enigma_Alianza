import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt

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
    """Calcula el desplazamiento trigonométrico según la función asignada"""
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
    """Ciclo rotatorio: 1ª letra -> SEN, 2ª -> COS, 3ª -> TAN"""
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

def generar_grafico_plano(x, y_orig, y_dest, char_orig, char_dest, op_nombre):
    """Genera una imagen del plano cartesiano 2D con Matplotlib"""
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Ejes cartesianos
    ax.axhline(0, color='gray', linewidth=1)
    ax.axvline(0, color='gray', linewidth=1)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Puntos en el plano
    ax.scatter([x], [y_orig], color='blue', s=100, label=f"Original '{char_orig}' ({x}, {y_orig})")
    ax.scatter([x], [y_dest], color='red', s=100, label=f"Transformado '{char_dest}' ({x}, {y_dest})")
    
    # Flecha de transformación
    ax.annotate('', xy=(x, y_dest), xytext=(x, y_orig),
                arrowprops=dict(facecolor='green', edgecolor='green', arrowstyle='->', lw=2))
    
    # Formato
    ax.set_xlim(0, max(10, x + 2))
    ax.set_ylim(0, 30)
    ax.set_xlabel("Posición en palabra (X)")
    ax.set_ylabel("Valor alfabético (Y)")
    ax.set_title(f"Plano Cartesiano — Función: {op_nombre}")
    ax.legend(loc="upper left")
    
    plt.tight_layout()
    return fig

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
    
    # Distribución en dos columnas
    col_izquierda, col_derecha = st.columns([1, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Controles")
        op = st.radio("Selecciona una opción:", ["Cifrar", "Descifrar"])
        msg = st.text_input("Introduce tu mensaje:")
        btn_ejecutar = st.button("Ejecutar")

    with col_derecha:
        st.subheader("🎬 Simulación visual del proceso")
        pantalla_simulacion = st.empty()
        pantalla_simulacion.info("Introduce un mensaje y pulsa 'Ejecutar' para ver el gráfico y los cálculos paso a paso.")

    # Ejecución de la animación
    if btn_ejecutar:
        if not msg.strip():
            st.warning("Por favor, introduce un texto válido.")
        else:
            modo = 'cifrar' if op == "Cifrar" else 'descifrar'
            res_final, pasos = procesar_trigonometrico_paso_a_paso(msg, modo)
            
            # Cálculo para que la animación dure aproximadamente 15 segundos en total
            num_pasos = len(pasos)
            tiempo_espera = 15.0 / num_pasos if num_pasos > 0 else 2.0
            tiempo_espera = max(1.5, tiempo_espera) # Al menos 1.5s por paso
            
            progreso_bar = col_derecha.progress(0)
            
            for i, paso in enumerate(pasos):
                progreso_bar.progress((i + 1) / num_pasos)
                
                # Generamos el gráfico cartesiano en directo
                fig = generar_grafico_plano(
                    x=paso['posicion'],
                    y_orig=paso['valor_original'],
                    y_dest=paso['resultado_num'],
                    char_orig=paso['original'],
                    char_dest=paso['resultado_char'],
                    op_nombre=paso['operacion']
                )
                
                with pantalla_simulacion.container():
                    st.markdown(f"#### Paso {i+1} de {num_pasos} — Letra: **'{paso['original']}'**")
                    
                    # Mostrar gráfico del plano cartesiano
                    st.pyplot(fig)
                    plt.close(fig)
                    
                    st.write(f"**Función:** `{paso['operacion']}` | **Ángulo:** `{paso['angulo_deg']:.1f}°` | **Desplazamiento:** `{'+' if modo == 'cifrar' else '-'}{paso['desplazamiento']}`")
                    st.latex(
                        rf"({paso['valor_original']} {'+' if modo == 'cifrar' else '-'} \text{{{paso['operacion']}}}(\theta)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                    )
                
                time.sleep(tiempo_espera)
                
            col_derecha.success("¡Proceso completado!")
            
            # Resultado final abajo
            st.divider()
            st.subheader("📌 Resultado Final")
            st.text_area("Mensaje obtenido:", value=res_final, help="Copia este mensaje")

    st.divider()
    if st.button("Cerrar sesión"):
        st.session_state.autenticado = False
        st.rerun()
