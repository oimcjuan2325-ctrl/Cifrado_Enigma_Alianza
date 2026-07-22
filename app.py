import streamlit as st
import numpy as np
import time
import json
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Inicie sesión en esta web", page_icon="🛡️", layout="wide")

# ==============================================================================
# 📧 CONFIGURACIÓN DE TU CORREO Y CUENTA LÍDER
# ==============================================================================
ADMIN_USER = "Juan"
ADMIN_PASS = "2325"
ADMIN_EMAIL = "oimc.juan2325@gmail.com"
GMAIL_EMISOR = "oimc.juan2325@gmail.com"  
PASSWORD_EMISOR = "ouagwqwvjetehcwu"  # Contraseña de aplicación de Google

DB_FILE = "usuarios_faccion.json"

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def obtener_fecha_actual():
    now = datetime.now()
    mes = MESES[now.month]
    return f"{now.day} de {mes} de {now.year}"

# --- FUNCIONES DE BASE DE DATOS Y CORREO ---
def cargar_usuarios():
    # Estructura base asegurando que Juan siempre exista como AUTORIZADO
    usuarios_base = {
        ADMIN_USER: {
            "gmail": ADMIN_EMAIL,
            "password": ADMIN_PASS,
            "estado": "AUTORIZADO",
            "fecha_autorizacion": "22 de julio de 2026"
        }
    }
    if not os.path.exists(DB_FILE):
        guardar_usuarios(usuarios_base)
        return usuarios_base
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            # Forzamos siempre que Juan esté en estado AUTORIZADO
            datos[ADMIN_USER] = usuarios_base[ADMIN_USER]
            return datos
    except:
        return usuarios_base

def guardar_usuarios(data):
    # Aseguramos que los datos de Juan no se sobreescriban nunca
    data[ADMIN_USER] = {
        "gmail": ADMIN_EMAIL,
        "password": ADMIN_PASS,
        "estado": "AUTORIZADO",
        "fecha_autorizacion": "22 de julio de 2026"
    }
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def enviar_email(destino, asunto, cuerpo):
    msg = MIMEText(cuerpo, 'plain', 'utf-8')
    msg['Subject'] = asunto
    msg['From'] = GMAIL_EMISOR
    msg['To'] = destino

    try:
        # Intento con SSL directo (Puerto 465)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
        server.sendmail(GMAIL_EMISOR, [destino], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        try:
            # Fallback a STARTTLS (Puerto 587) por si el hosting bloquea el puerto 465
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
            server.starttls()
            server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
            server.sendmail(GMAIL_EMISOR, [destino], msg.as_string())
            server.quit()
            return True
        except Exception as e2:
            return False

def enviar_notificacion_admin(gmail_solicitante, usuario_solicitante):
    asunto = f"🚨 ALERTA FACCIÓN: Nueva solicitud de registro de {usuario_solicitante}"
    cuerpo = f"""
Se ha registrado una nueva solicitud en la web:

- Usuario: {usuario_solicitante}
- Gmail: {gmail_solicitante}

Inicia sesión en la web con tu cuenta de Líder para AUTORIZAR o NO AUTORIZAR el acceso.
"""
    enviar_email(ADMIN_EMAIL, asunto, cuerpo)

def enviar_confirmacion_usuario(gmail_destino, usuario, password, estado):
    if estado == "AUTORIZADO":
        asunto = "✅ Cuenta Autorizada - Inicie sesión en esta web"
        cuerpo = f"""Felicitaciones, ya puede iniciar sesión con esta cuenta y con la contraseña la cual inició sesión anteriormente.

----------------------------------------
📌 SUS DATOS DE ACCESO:
• Nombre de usuario: {usuario}
• Contraseña: {password}
----------------------------------------

Ya puede acceder a la web e iniciar sesión.
"""
    else:
        asunto = "❌ Estado de Solicitud de Cuenta"
        cuerpo = f"""Lo sentimos mucho, pero su cuenta ({usuario}) no ha sido autorizada por el Administrador. 

Por favor, inténtelo de nuevo más tarde o contacte con el Administrador.
"""
    enviar_email(gmail_destino, asunto, cuerpo)

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
    .notice-box {
        background-color: #0e2a38;
        color: #a3e5ff;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #00aaff;
        font-size: 18px;
        text-align: center;
        margin-top: 20px;
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
if 'modo_pantalla' not in st.session_state: st.session_state.modo_pantalla = "login"

db_usuarios = cargar_usuarios()

# --- PANTALLA DE ACCESO Y REGISTRO ---
if not st.session_state.autenticado:

    # 1. MODO: MENSAJE DE ESPERA POST-REGISTRO
    if st.session_state.modo_pantalla == "registro_completado":
        st.markdown("""
        <div class="notice-box">
            <h2>📩 Solicitud enviada con éxito</h2>
            <p>Tiene que esperar hasta que se le autorice la cuenta.</p>
            <p>Cuando tenga autorizada o no autorizada la cuenta, se le mandará un Gmail, por favor, esté atento al Gmail.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("⬅️ Volver al Inicio de Sesión"):
            st.session_state.modo_pantalla = "login"
            st.rerun()

    # 2. MODO: CREAR CUENTA NUEVA
    elif st.session_state.modo_pantalla == "registro":
        st.title("Crear cuenta nueva")
        
        reg_gmail = st.text_input("Introduce el Gmail deseado:", key="reg_gmail")
        reg_user = st.text_input("Nombre de usuario:", key="reg_user")
        reg_pass = st.text_input("Contraseña:", type="password", key="reg_pass")
        
        st.write("")
        col_reg1, col_reg2 = st.columns([1, 2])
        with col_reg1:
            if st.button("Crear cuenta", key="btn_reg"):
                if not reg_gmail or not reg_user or not reg_pass:
                    st.warning("Por favor, rellene todos los campos.")
                elif "@" not in reg_gmail:
                    st.error("Lo sentimos mucho, pero esta cuenta no se puede utilizar. Elija otro Gmail.")
                elif reg_user == ADMIN_USER or reg_user in db_usuarios:
                    st.error("Ese nombre de usuario ya está ocupado. Elija otro.")
                else:
                    db_usuarios[reg_user] = {
                        "gmail": reg_gmail,
                        "password": reg_pass,
                        "estado": "PENDIENTE",
                        "fecha_autorizacion": ""
                    }
                    guardar_usuarios(db_usuarios)
                    enviar_notificacion_admin(reg_gmail, reg_user)
                    st.session_state.modo_pantalla = "registro_completado"
                    st.rerun()
        with col_reg2:
            if st.button("Cancelar y volver"):
                st.session_state.modo_pantalla = "login"
                st.rerun()

    # 3. MODO: INICIO DE SESIÓN (POR DEFECTO)
    else:
        st.title("Inicie sesión en esta web")
        st.subheader("Inicio de sesión")
        
        u_login = st.text_input("Nombre:", key="login_user")
        p_login = st.text_input("Contraseña:", type="password", key="login_pass")
        
        st.write("")
        if st.button("Iniciar sesión", key="btn_login"):
            # REGLA DIOS: Si eres Juan con contraseña 2325 entras directo SIEMPRE
            if u_login == ADMIN_USER and p_login == ADMIN_PASS:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = ADMIN_USER
                st.success("Acceso concedido como Líder Principal.")
                time.sleep(1)
                st.rerun()
            elif u_login in db_usuarios:
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

        st.divider()
        if st.button("🔗 Crear una cuenta nueva", type="secondary"):
            st.session_state.modo_pantalla = "registro"
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
    
    # --- SECCIÓN EXCLUSIVA DE LÍDER ---
    es_lider = (st.session_state.usuario_actual == ADMIN_USER)
    
    if es_lider:
        with st.expander("👑 PANEL DE LÍDER", expanded=True):
            tab_pend, tab_aut, tab_no_aut = st.tabs([
                "⏳ Cuentas en proceso de autorización", 
                "✅ Cuentas ya autorizadas", 
                "❌ Cuentas no autorizadas"
            ])
            
            # 1. CUENTAS EN PROCESO DE AUTORIZACIÓN
            with tab_pend:
                pendientes = {u: d for u, d in db_usuarios.items() if d["estado"] == "PENDIENTE" and u != ADMIN_USER}
                if not pendientes:
                    st.info("No hay ninguna cuenta en proceso de autorización.")
                else:
                    for usr, data in pendientes.items():
                        c1, c2, c3 = st.columns([2, 1, 1])
                        with c1:
                            st.write(f"👤 **{usr}** (`{data['gmail']}`)")
                        with c2:
                            if st.button(f"✅ Autorizar", key=f"aut_{usr}"):
                                fecha_hoy = obtener_fecha_actual()
                                db_usuarios[usr]["estado"] = "AUTORIZADO"
                                db_usuarios[usr]["fecha_autorizacion"] = fecha_hoy
                                guardar_usuarios(db_usuarios)
                                enviar_confirmacion_usuario(data["gmail"], usr, data["password"], "AUTORIZADO")
                                st.success(f"{usr} autorizado el {fecha_hoy} y notificado.")
                                time.sleep(1)
                                st.rerun()
                        with c3:
                            if st.button(f"❌ No Autorizar", key=f"no_aut_{usr}"):
                                db_usuarios[usr]["estado"] = "RECHAZADO"
                                guardar_usuarios(db_usuarios)
                                enviar_confirmacion_usuario(data["gmail"], usr, data["password"], "RECHAZADO")
                                st.error(f"{usr} rechazado y notificado.")
                                time.sleep(1)
                                st.rerun()
                        st.divider()

            # 2. CUENTAS YA AUTORIZADAS
            with tab_aut:
                autorizadas = {u: d for u, d in db_usuarios.items() if d["estado"] == "AUTORIZADO"}
                if not autorizadas:
                    st.info("No hay cuentas autorizadas.")
                else:
                    for usr, data in autorizadas.items():
                        c1, c2 = st.columns([3, 1])
                        fecha_str = data.get("fecha_autorizacion", "Fecha no registrada")
                        with c1:
                            st.write(f"👤 **{usr}** (`{data['gmail']}`) — Autorizado el: `{fecha_str}`")
                        with c2:
                            if usr != ADMIN_USER:
                                if st.button(f"🚫 Desautorizar esta cuenta", key=f"desaut_{usr}"):
                                    db_usuarios[usr]["estado"] = "RECHAZADO"
                                    guardar_usuarios(db_usuarios)
                                    st.warning(f"Se ha desautorizado la cuenta {usr}.")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.caption("👑 Cuenta Líder Principal")
                        st.divider()

            # 3. CUENTAS NO AUTORIZADAS
            with tab_no_aut:
                no_autorizadas = {u: d for u, d in db_usuarios.items() if d["estado"] == "RECHAZADO" and u != ADMIN_USER}
                if not no_autorizadas:
                    st.info("No hay cuentas rechazadas/no autorizadas.")
                else:
                    for usr, data in no_autorizadas.items():
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.write(f"👤 **{usr}** (`{data['gmail']}`)")
                        with c2:
                            if st.button(f"✅ Autorizar esta cuenta", key=f"re_aut_{usr}"):
                                fecha_hoy = obtener_fecha_actual()
                                db_usuarios[usr]["estado"] = "AUTORIZADO"
                                db_usuarios[usr]["fecha_autorizacion"] = fecha_hoy
                                guardar_usuarios(db_usuarios)
                                enviar_confirmacion_usuario(data["gmail"], usr, data["password"], "AUTORIZADO")
                                st.success(f"{usr} ha sido autorizada el {fecha_hoy}.")
                                time.sleep(1)
                                st.rerun()
                        st.divider()

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
        st.session_state.modo_pantalla = "login"
        st.rerun()
