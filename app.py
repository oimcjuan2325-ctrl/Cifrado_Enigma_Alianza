from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
import base64
import json
import os
import smtplib
import time
import urllib.request
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Terminal de Cifrado Facción", page_icon="🛡️", layout="wide"
)

# ==============================================================================
# 🐙 CONFIGURACIÓN DE GITHUB COMO BASE DE DATOS
# ==============================================================================
try:
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    GITHUB_REPO = st.secrets["GITHUB_REPO"]
    GITHUB_PATH = st.secrets.get("GITHUB_PATH", "usuarios_faccion.json")
    USAR_GITHUB = True
except Exception:
    USAR_GITHUB = False

ADMIN_USER = "Juan"
ADMIN_PASS = "2325"
ADMIN_EMAIL = "oimcjuan2325@gmail.com"
GMAIL_EMISOR = "oimcjuan2325@gmail.com"
PASSWORD_EMISOR = "ouagwqwvjetehcwu"

DB_FILE = "usuarios_faccion.json"

MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def obtener_fecha_actual():
    now = datetime.now()
    mes = MESES[now.month]
    return f"{now.day} de {mes} de {now.year}"


def cargar_usuarios():
    if "db_usuarios_memoria" in st.session_state:
        return st.session_state.db_usuarios_memoria

    usuarios_base = {
        ADMIN_USER: {
            "gmail": ADMIN_EMAIL,
            "password": ADMIN_PASS,
            "estado": "AUTORIZADO",
            "fecha_autorizacion": "22 de julio de 2026",
            "bloqueo_hasta": None,
        }
    }

    if USAR_GITHUB:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}"
            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Streamlit-App",
                },
            )
            with urllib.request.urlopen(req) as response:
                data_json = json.loads(response.read().decode("utf-8"))
                contenido_decodificado = base64.b64decode(
                    data_json["content"]
                ).decode("utf-8")
                datos = json.loads(contenido_decodificado)
                datos[ADMIN_USER] = usuarios_base[ADMIN_USER]
                st.session_state.db_usuarios_memoria = datos
                return datos
        except Exception:
            pass

    if not os.path.exists(DB_FILE):
        guardar_usuarios(usuarios_base)
        return usuarios_base
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            datos = json.load(f)
            datos[ADMIN_USER] = usuarios_base[ADMIN_USER]
            st.session_state.db_usuarios_memoria = datos
            return datos
    except:
        st.session_state.db_usuarios_memoria = usuarios_base
        return usuarios_base


def guardar_usuarios(data):
    data[ADMIN_USER] = {
        "gmail": ADMIN_EMAIL,
        "password": ADMIN_PASS,
        "estado": "AUTORIZADO",
        "fecha_autorizacion": "22 de julio de 2026",
        "bloqueo_hasta": None,
    }
    st.session_state.db_usuarios_memoria = data
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

    if USAR_GITHUB:
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_PATH}"
            req_get = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json",
                    "User-Agent": "Streamlit-App",
                },
            )
            sha = None
            try:
                with urllib.request.urlopen(req_get) as resp:
                    sha = json.loads(resp.read().decode("utf-8"))["sha"]
            except:
                pass

            contenido_str = json.dumps(data, ensure_ascii=False, indent=4)
            contenido_bytes = base64.b64encode(contenido_str.encode("utf-8")).decode(
                "utf-8"
            )
            payload = {
                "message": "Actualización de usuarios",
                "content": contenido_bytes,
            }
            if sha:
                payload["sha"] = sha
            req_put = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"token {GITHUB_TOKEN}",
                    "Accept": "application/vnd.github.v3+json",
                    "Content-Type": "application/json",
                    "User-Agent": "Streamlit-App",
                },
                method="PUT",
            )
            urllib.request.urlopen(req_put)
        except Exception:
            pass


def enviar_email(destino, asunto, cuerpo):
    msg = MIMEText(cuerpo, "plain", "utf-8")
    msg["Subject"] = Header(asunto, "utf-8")
    msg["From"] = GMAIL_EMISOR
    msg["To"] = destino
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.starttls()
        server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
        server.sendmail(GMAIL_EMISOR, [destino], msg.as_string())
        server.quit()
        return True
    except:
        return False


def enviar_notificacion_admin(gmail_solicitante, usuario_solicitante):
    asunto = f"🚨 ALERTA FACCIÓN: Nueva solicitud de {usuario_solicitante}"
    cuerpo = f"Usuario: {usuario_solicitante}\nGmail: {gmail_solicitante}"
    enviar_email(ADMIN_EMAIL, asunto, cuerpo)


def enviar_confirmacion_usuario(gmail_destino, usuario, password, estado):
    if estado == "AUTORIZADO":
        asunto = "✅ Cuenta Autorizada"
        cuerpo = f"Ya puede iniciar sesión.\nUsuario: {usuario}\nContraseña: {password}"
    else:
        asunto = "❌ Cuenta No Autorizada"
        cuerpo = "Su cuenta no ha sido autorizada."
    enviar_email(gmail_destino, asunto, cuerpo)


# ==============================================================================
# 🌀 MOTOR CRIPTOGRÁFICO BASADO EN EL NÚMERO MÁS IRRACIONAL (PHI: 1.618...)
# ==============================================================================
def obtener_motor_irracional():
    """Deriva de forma interna la clave criptográfica usando

    la constante exacta del Número Áureo (el más irracional).
    """
    # El número irracional más seguro y perfecto incrustado directamente como clave del sistema
    numero_ureo_mas_irracional = (
        "1.61803398874989484820458683436563811772030917980576286213544862270526046"
    )
    sal_sistema = b"faccion_phi_absoluto_seed"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sal_sistema,
        iterations=100000,
    )
    clave_derivada = base64.urlsafe_b64encode(
        kdf.derive(numero_ureo_mas_irracional.encode("utf-8"))
    )
    return Fernet(clave_derivada)


def cifrar_automatico(texto_claro):
    """Cifra usando el número áureo de fondo de forma completamente transparente."""
    f = obtener_motor_irracional()
    return f.encrypt(texto_claro.encode("utf-8")).decode("utf-8")


def descifrar_automatico(texto_cifrado):
    """Descifra usando exactamente el mismo número áureo de fondo."""
    f = obtener_motor_irracional()
    return f.decrypt(texto_cifrado.encode("utf-8")).decode("utf-8")


# --- ESTILOS CSS ---
st.markdown(
    """
<style>
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
    .permanent-warning {
        background-color: #4a0000;
        color: #ffb3b3;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff3333;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- ESTADOS DE SESIÓN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "modo_pantalla" not in st.session_state:
    st.session_state.modo_pantalla = "login"

db_usuarios = cargar_usuarios()

# --- PANTALLAS DE ACCESO ---
if not st.session_state.autenticado:
    if st.session_state.modo_pantalla == "registro_completado":
        st.markdown(
            """
            <div class="notice-box">
                <h2>📩 Solicitud enviada con éxito</h2>
                <p>Tiene que esperar hasta que se le autorice la cuenta. Esté atento a su correo.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("⬅️ Volver al Inicio de Sesión"):
            st.session_state.modo_pantalla = "login"
            st.rerun()

    elif st.session_state.modo_pantalla == "registro":
        st.title("Crear cuenta nueva")
        reg_gmail = st.text_input("Gmail deseado:", key="reg_gmail")
        reg_user = st.text_input("Nombre de usuario:", key="reg_user")
        reg_pass = st.text_input("Contraseña:", type="password", key="reg_pass")
        if st.button("Crear cuenta"):
            if not reg_gmail or not reg_user or not reg_pass:
                st.warning("Rellene todos los campos.")
            elif reg_user in db_usuarios:
                st.error("El usuario ya existe.")
            else:
                db_usuarios[reg_user] = {
                    "gmail": reg_gmail,
                    "password": reg_pass,
                    "estado": "PENDIENTE",
                    "fecha_autorizacion": "",
                    "bloqueo_hasta": None,
                }
                guardar_usuarios(db_usuarios)
                enviar_notificacion_admin(reg_gmail, reg_user)
                st.session_state.modo_pantalla = "registro_completado"
                st.rerun()
        if st.button("Cancelar"):
            st.session_state.modo_pantalla = "login"
            st.rerun()

    elif st.session_state.modo_pantalla == "cierre_permanente":
        st.title("Cerrar sesión permanente")
        st.markdown(
            """
            <div class="permanent-warning">
                ⚠️ ADVERTENCIA: Bloqueará su cuenta durante 5 días (120 horas).
            </div>
            """,
            unsafe_allow_html=True,
        )
        perm_gmail = st.text_input("Gmail:", key="p_gmail")
        perm_user = st.text_input("Usuario:", key="p_user")
        perm_pass = st.text_input("Contraseña:", type="password", key="p_pass")
        if st.button("Ejecutar cierre"):
            if (
                perm_user in db_usuarios
                and db_usuarios[perm_user]["gmail"] == perm_gmail
                and db_usuarios[perm_user]["password"] == perm_pass
            ):
                db_usuarios[perm_user]["bloqueo_hasta"] = (
                    datetime.now() + timedelta(hours=120)
                ).isoformat()
                guardar_usuarios(db_usuarios)
                st.success("Cuenta bloqueada temporalmente.")
                time.sleep(2)
                st.session_state.modo_pantalla = "login"
                st.rerun()
            else:
                st.error("Datos incorrectos.")
        if st.button("Volver"):
            st.session_state.modo_pantalla = "login"
            st.rerun()

    else:
        st.title("Inicie sesión en esta web")
        u_login = st.text_input("Nombre:", key="l_user")
        p_login = st.text_input("Contraseña:", type="password", key="l_pass")
        if st.button("Iniciar sesión"):
            if u_login == ADMIN_USER and p_login == ADMIN_PASS:
                st.session_state.autenticado = True
                st.session_state.usuario_actual = ADMIN_USER
                st.rerun()
            elif u_login in db_usuarios:
                usr_data = db_usuarios[u_login]
                if usr_data.get("bloqueo_hasta"):
                    if datetime.now() < datetime.fromisoformat(
                        usr_data["bloqueo_hasta"]
                    ):
                        st.error("Cuenta bloqueada temporalmente.")
                        st.stop()
                if (
                    usr_data["password"] == p_login
                    and usr_data["estado"] == "AUTORIZADO"
                ):
                    st.session_state.autenticado = True
                    st.session_state.usuario_actual = u_login
                    st.rerun()
                else:
                    st.error("Datos incorrectos o cuenta no autorizada.")
            else:
                st.error("El usuario no existe.")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Crear cuenta nueva"):
                st.session_state.modo_pantalla = "registro"
                st.rerun()
        with c2:
            if st.button("Cierre permanente"):
                st.session_state.modo_pantalla = "cierre_permanente"
                st.rerun()

# --- PANTALLA PRINCIPAL ---
else:
    st.markdown(
        """
    <div class="warning-banner">
        ⚠️ ADVERTENCIA: Está estrictamente prohibido revelar información confidencial de esta web bajo sanción de inhabilitación permanente.
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.title("📟 Terminal de Transmisión")
    st.caption(f"Sesión iniciada como: `{st.session_state.usuario_actual}`")

    if st.session_state.usuario_actual == ADMIN_USER:
        with st.expander("👑 PANEL DE LÍDER", expanded=True):
            tab_pend, tab_aut, tab_no_aut = st.tabs(
                [
                    "⏳ Pendientes",
                    "✅ Autorizadas",
                    "❌ Rechazadas",
                ]
            )
            with tab_pend:
                pendientes = {
                    u: d
                    for u, d in db_usuarios.items()
                    if d["estado"] == "PENDIENTE" and u != ADMIN_USER
                }
                if not pendientes:
                    st.info("No hay solicitudes pendientes.")
                else:
                    for usr, data in pendientes.items():
                        c1, c2, c3 = st.columns([2, 1, 1])
                        with c1:
                            st.write(f"👤 {usr} (`{data['gmail']}`)")
                        with c2:
                            if st.button("Autorizar", key=f"aut_{usr}"):
                                db_usuarios[usr]["estado"] = "AUTORIZADO"
                                db_usuarios[usr][
                                    "fecha_autorizacion"
                                ] = obtener_fecha_actual()
                                guardar_usuarios(db_usuarios)
                                enviar_confirmacion_usuario(
                                    data["gmail"],
                                    usr,
                                    data["password"],
                                    "AUTORIZADO",
                                )
                                st.rerun()
                        with c3:
                            if st.button("Rechazar", key=f"rec_{usr}"):
                                db_usuarios[usr]["estado"] = "RECHAZADO"
                                guardar_usuarios(db_usuarios)
                                enviar_confirmacion_usuario(
                                    data["gmail"],
                                    usr,
                                    data["password"],
                                    "RECHAZADO",
                                )
                                st.rerun()

            with tab_aut:
                for usr, data in db_usuarios.items():
                    if data["estado"] == "AUTORIZADO" and usr != ADMIN_USER:
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.write(f"👤 {usr} (`{data['gmail']}`)")
                        with c2:
                            if st.button("Desautorizar", key=f"des_{usr}"):
                                db_usuarios[usr]["estado"] = "RECHAZADO"
                                guardar_usuarios(db_usuarios)
                                st.rerun()

            with tab_no_aut:
                for usr, data in db_usuarios.items():
                    if data["estado"] == "RECHAZADO" and usr != ADMIN_USER:
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.write(f"👤 {usr} (`{data['gmail']}`)")
                        with c2:
                            if st.button("Re-autorizar", key=f"reaut_{usr}"):
                                db_usuarios[usr]["estado"] = "AUTORIZADO"
                                guardar_usuarios(db_usuarios)
                                st.rerun()

    st.divider()

    st.subheader(
        "⚙️ Cifrado y Descifrado con el Número Áureo (Automático y Sin Claves)"
    )
    tab_cifrar, tab_descifrar = st.tabs(["🔒 Cifrar", "🔓 Descifrar"])

    with tab_cifrar:
        msg_claro = st.text_area(
            "Mensaje a proteger:", key="input_cifrar_texto"
        )
        if st.button("Cifrar con Número Áureo"):
            if not msg_claro.strip():
                st.warning("Introduce un mensaje.")
            else:
                try:
                    codigo_cifrado = cifrar_automatico(msg_claro)
                    st.success(
                        "¡Mensaje cifrado mediante la constante del número más irracional!"
                    )
                    st.write("Resultado cifrado:")
                    st.code(codigo_cifrado, language="text")
                    st.caption(
                        "Clave aplicada de forma totalmente autónoma por el sistema."
                    )
                except Exception as e:
                    st.error(f"Error al cifrar: {e}")

    with tab_descifrar:
        msg_cifrado_input = st.text_area(
            "Pega aquí el código cifrado:", key="input_msg_descifrar"
        )
        if st.button("Descifrar con Número Áureo"):
            if not msg_cifrado_input.strip():
                st.warning("Introduce el código cifrado.")
            else:
                try:
                    resultado = descifrar_automatico(msg_cifrado_input.strip())
                    st.success("¡Descifrado exitoso!")
                    st.markdown(f"**Mensaje original:** `{resultado}`")
                except Exception:
                    st.error(
                        "Error: Código inválido o corrupto (imposible revertir)."
                    )

    st.divider()
    if st.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.session_state.usuario_actual = ""
        st.session_state.modo_pantalla = "login"
        st.rerun()
