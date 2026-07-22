import streamlit as st
import numpy as np
import time
import json
import os
import smtplib
from email.mime.text import MIMEText

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Cifrado Trigonométrico - Red de Defensa", page_icon="🛡️", layout="wide")

# ==============================================================================
# 📧 CONFIGURACIÓN DE TU CORREO (ADMINISTRADOR)
# ==============================================================================
ADMIN_EMAIL = "oimcjuan2325@gmail.com"
GMAIL_EMISOR = "oimcjuan2325@gmail.com"  
PASSWORD_EMISOR = "ouagwqwvjetehcwu"  # Contraseña de aplicación de Google configurada

DB_FILE = "usuarios_faccion.json"

# --- FUNCIONES DE BASE DE DATOS (PERSISTENTE) ---
def cargar_usuarios():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def guardar_usuarios(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def enviar_notificacion_admin(gmail_solicitante, usuario_solicitante):
    asunto = f"🚨 ALERTA FACCIÓN: Nueva solicitud de registro de {usuario_solicitante}"
    cuerpo = f"""
    Este correo ha intentado iniciar sesión/crear cuenta en la web:
    
    - Usuario: {usuario_solicitante}
    - Gmail introducido: {gmail_solicitante}
    
    Por favor, entra al panel de administración de la web para Autorizar o No Autorizar esta cuenta.
    """
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = GMAIL_EMISOR
    msg['To'] = ADMIN_EMAIL

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
        server.sendmail(GMAIL_EMISOR, [ADMIN_EMAIL], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

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
    .warning-banner {
        background-color: #3d0000;
        color: #ff4d4d;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #ff0000;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
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
    else:
        val = np.tan(angulo_rad)
        
    desplazamiento = int(np.round(val * 10))
    if desplazamiento == 0:
        desplazamiento = 1
    return desplazamiento

def obtener_operacion(idx_letra):
    operaciones = ['SEN', 'COS', 'TAN']
    return operaciones[idx_letra % 3]

def texto_a_binario(texto):
    return " ".join(format(ord(c), '08b') for c in texto)

def binario_a_texto(cadena_binaria):
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

# --- ESTADOS DE SESIÓN ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if 'usuario_actual' not in st.session_state: st.session_state.usuario_actual = ""

db_usuarios = cargar_usuarios()

# --- PANTALLA DE ACCESO Y REGISTRO ---
if not st.session_state.autenticado:
    st.title("Inicie sesión al cifrado trigonométrico + transmisión binaria")
    
    tab1, tab2, tab_admin = st.tabs(["🔑 Ya tengo una cuenta", "📝 Crear una cuenta", "👑 Panel Líder"])
    
    # --- TAB 1: INICIO DE SESIÓN ---
    with tab1:
        st.subheader("Acceso a usuarios registrados")
        u_login = st.text_input("Nombre de usuario:", key="login_user")
        p_login = st.text_input("Contraseña:", type="password", key="login_pass")
        
        if st.button("Iniciar Sesión", key="btn_login"):
            if u_login in db_usuarios:
                usr_data = db_usuarios[u_login]
                if usr_data["password"] == p_login:
                    if usr_data["estado"] == "AUTORIZADO":
                        st.session_state.autenticado = True
                        st.session_state.usuario_actual = u_login
                        st.success("Está de buena suerte. Su cuenta ha sido autorizada. Ya puede acceder a esta web.")
                        time.sleep(1.5)
                        st.rerun()
                    elif usr_data["estado"] == "RECHAZADO":
                        st.error("Lo sentimos mucho, pero su cuenta no ha sido autorizada. Por favor, inténtelo de nuevo.")
                    else:
                        st.info("Su cuenta está pendiente de revisión por el Administrador. Vuelva a intentarlo más tarde.")
                else:
                    st.warning("Contraseña incorrecta.")
            else:
                st.error("El usuario no existe. Por favor, cree una cuenta.")

    # --- TAB 2: REGISTRO DE NUEVA CUENTA ---
    with tab2:
        st.subheader("Formulario de registro")
        reg_gmail = st.text_input("Escriba su Gmail (el cual está autorizado):", key="reg_gmail")
        reg_user = st.text_input("Escriba el nombre de usuario que desee:", key="reg_user")
        reg_pass = st.text_input("Escriba su contraseña:", type="password", key="reg_pass")
        
        if st.button("Crear cuenta", key="btn_reg"):
            if not reg_gmail or not reg_user or not reg_pass:
                st.warning("Por favor, rellene todos los campos.")
            elif "@" not in reg_gmail:
                st.error("Lo sentimos mucho, pero esta cuenta no se puede utilizar. Elija otro Gmail.")
            elif reg_user in db_usuarios:
                st.error("Ese nombre de usuario ya está ocupado. Elija otro.")
            else:
                db_usuarios[reg_user] = {
                    "gmail": reg_gmail,
                    "password": reg_pass,
                    "estado": "PENDIENTE"
                }
                guardar_usuarios(db_usuarios)
                enviar_notificacion_admin(reg_gmail, reg_user)
                st.info("Su solicitud ha sido enviada al Líder para su verificación. Cuando revise su cuenta, podrá iniciar sesión.")

    # --- TAB 3: PANEL DEL LÍDER ---
    with tab_admin:
        st.subheader("🔒 Gestión de Autorizaciones (Líder)")
        admin_pass = st.text_input("Contraseña Máxima del Líder:", type="password", key="pass_admin")
        
        if admin_pass == "MAQUINA":
            st.success("Panel de Administrador Desbloqueado.")
            
            pendientes = {u: d for u, d in db_usuarios.items() if d["estado"] == "PENDIENTE"}
            
            if not pendientes:
                st.write("No hay cuentas pendientes de revisión.")
            else:
                for usr, data in pendientes.items():
                    st.write(f"👤 **Usuario:** `{usr}` | 📧 **Gmail:** `{data['gmail']}`")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"✅ Autorizar a {usr}", key=f"aut_{usr}"):
                            db_usuarios[usr]["estado"] = "AUTORIZADO"
                            guardar_usuarios(db_usuarios)
                            st.success(f"{usr} ha sido AUTORIZADO con éxito.")
                            st.rerun()
                    with col_b:
                        if st.button(f"❌ No Autorizar a {usr}", key=f"no_aut_{usr}"):
                            db_usuarios[usr]["estado"] = "RECHAZADO"
                            guardar_usuarios(db_usuarios)
                            st.error(f"{usr} ha sido RECHAZADO.")
                            st.rerun()

# --- PANTALLA PRINCIPAL DE LA APLICACIÓN ---
else:
    st.markdown("""
    <div class="warning-banner">
        ⚠️ ADVERTENCIA: Ten cuidado con la información que revelas de esta web. Está estrictamente prohibido revelar información sobre esta web. Por favor, si revela algún tipo de información de esta web, será sancionado con una inhabilitación permanente de la cuenta.
    </div>
    """, unsafe_allow_html=True)
    
    st.title("📟 Terminal de Cifrado y Transmisión")
    st.caption(f"Sesión iniciada como: `{st.session_state.usuario_actual}`")
    
    col_izquierda, col_derecha = st.columns([1, 1], gap="large")
    
    with col_izquierda:
        st.subheader("⚙️ Controles de Operación")
        op = st.radio("Acción a realizar:", ["Cifrar", "Descifrar"])
        msg = st.text_input("Mensaje (Texto o Cadenas Binarias):")
        btn_ejecutar = st.button("Procesar y Transmitir")

    with col_derecha:
        st.subheader("🎬 Estado de la Transmisión")
        pantalla_simulacion = st.empty()
        pantalla_simulacion.info("Introduce un mensaje para iniciar el cifrado/descifrado en vivo.")

    if btn_ejecutar:
        if not msg.strip():
            st.warning("Por favor, introduce un texto válido.")
        else:
            modo = 'cifrar' if op == "Cifrar" else 'descifrar'
            res_trig, pasos = procesar_trigonometrico_paso_a_paso(msg, modo)
            
            num_pasos = len(pasos) + 1
            tiempo_espera = max(1.2, 12.0 / num_pasos)
            
            progreso_bar = col_derecha.progress(0)
            
            for i, paso in enumerate(pasos):
                progreso_bar.progress((i + 1) / num_pasos)
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {i+1} de {num_pasos} — Procesando: **'{paso['original']}'**")
                    
                    if modo == 'cifrar':
                        st.metric("Letra origen", f"{paso['original']} (Posición: {paso['valor_original']})")
                        st.write(f"**Cálculo:** `{paso['operacion']}({paso['valor_original']}°)` | **Desplazamiento:** `+{paso['desplazamiento']}`")
                        st.latex(
                            rf"({paso['valor_original']} + \text{{{paso['operacion']}}}({paso['valor_original']}^\circ)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                        )
                    else:
                        st.metric("Letra recibida", f"{paso['original']} (Posición: {paso['valor_original']})")
                        st.write(f"**Búsqueda inversa con:** `{paso['operacion']}` | **Desplazamiento:** `-{paso['desplazamiento']}`")
                        st.latex(
                            rf"({paso['valor_original']} - \text{{{paso['operacion']}}}(\text{{origen}}^\circ)) \pmod{{27}} = {paso['resultado_num']} \rightarrow \mathbf{{{paso['resultado_char']}}}"
                        )
                
                time.sleep(tiempo_espera)
                
            progreso_bar.progress(1.0)
            
            if modo == 'cifrar':
                res_binario = texto_a_binario(res_trig)
                res_final_output = res_binario
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {num_pasos} de {num_pasos} — ⚡ Conversión de Datos a Pulsos Binarios")
                    
                    st.markdown(f"""
                    <div class="matrix-box">
                        <div class="matrix-rain">01100101 01110011 01110100 01101111 00100000 01100101 01110011</div>
                        <br>
                        <div>CAPA TRIGONOMÉTRICA: <span style="color:#ffffff;">{res_trig}</span></div>
                        <br>
                        <div class="matrix-text">⚡ PAQUETE BINARIO SEGURO ⚡</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.code(res_binario, language="text")
            else:
                res_final_output = res_trig
                
                with pantalla_simulacion.container():
                    st.markdown(f"### Paso {num_pasos} de {num_pasos} — 🔓 Mensaje Decodificado")
                    st.markdown(f"""
                    <div class="matrix-box">
                        <div class="matrix-text">MENSAJE ORIGINAL RECUPERADO</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(res_trig, language="text")
            
            time.sleep(2.0)
            col_derecha.success("¡Operación completada con éxito!")
            
            st.divider()
            st.subheader("📌 Salida del Mensaje")
            st.text_area("Resultado:", value=res_final_output, help="Copia este texto para transmitirlo")

    st.divider()
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.rerun()
