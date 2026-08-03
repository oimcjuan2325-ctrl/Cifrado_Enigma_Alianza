from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText
import base64
import json
import os
import smtplib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Terminal de Cifrado Facción", page_icon="🛡️", layout="wide"
)

# ==============================================================================
# 📧 CONFIGURACIÓN DE CORREO Y LÍDER
# ==============================================================================
ADMIN_USER = "Juan"
ADMIN_PASS = "2325"
ADMIN_EMAIL = "oimcjuan2325@gmail.com"
GMAIL_EMISOR = "oimcjuan2325@gmail.com"
PASSWORD_EMISOR = "ouagwqwvjetehcwu"  # Contraseña de aplicación de Google

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


# --- FUNCIONES DE VALIDACIÓN Y DERIVACIÓN DE CLAVE ---
def validar_frase_segura(frase: str) -> tuple[bool, str]:
  """Valida que cada palabra de la frase tenga un mínimo de 10 caracteres."""
  if not frase or not frase.strip():
    return False, "La frase no puede estar vacía."

  palabras = frase.strip().split()
  for palabra in palabras:
    if len(palabra) < 10:
      return (
          False,
          f"⚠️ La palabra '{palabra}' tiene menos de 10 caracteres ({len(palabra)}). Cada palabra debe tener al menos 10 caracteres para mayor seguridad.",
      )
  return True, ""


def generar_clave_desde_frase(frase_secreta: str) -> bytes:
  """Deriva una clave segura de Fernet a partir de la frase validada."""
  salt = b"faccion_salt_seguridad_2026"
  kdf = PBKDF2HMAC(
      algorithm=hashes.SHA256(),
      length=32,
      salt=salt,
      iterations=100000,
  )
  return base64.urlsafe_b64encode(kdf.derive(frase_secreta.encode()))


# --- FUNCIONES DE BASE DE DATOS Y CORREO ---
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


def enviar_email(destino, asunto, cuerpo):
  msg = MIMEText(cuerpo, "plain", "utf-8")
  msg["Subject"] = Header(asunto, "utf-8")
  msg["From"] = GMAIL_EMISOR
  msg["To"] = destino

  try:
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
    server.sendmail(GMAIL_EMISOR, [destino], msg.as_string())
    server.quit()
    return True
  except Exception:
    try:
      server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15)
      server.login(GMAIL_EMISOR, PASSWORD_EMISOR)
      server.sendmail(GMAIL_EMISOR, [destino], msg.as_string())
      server.quit()
      return True
    except Exception:
      return False


def enviar_notificacion_admin(gmail_solicitante, usuario_solicitante):
  asunto = (
      f"🚨 ALERTA FACCIÓN: Nueva solicitud de registro de {usuario_solicitante}"
  )
  cuerpo = f"""Se ha registrado una nueva solicitud en la web:

- Usuario: {usuario_solicitante}
- Gmail: {gmail_solicitante}

Inicia sesión en la web con tu cuenta de Líder para AUTORIZAR o NO AUTORIZAR el acceso."""
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

Ya puede acceder a la web e iniciar sesión."""
  else:
    asunto = "❌ Estado de Solicitud de Cuenta"
    cuerpo = f"""Lo sentimos mucho, pero su cuenta ({usuario}) no ha sido autorizada por el Administrador. 

Por favor, inténtelo de nuevo más tarde o contacte con el Administrador."""
  enviar_email(gmail_destino, asunto, cuerpo)


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
    .key-warning {
        background-color: #4a2c00;
        color: #ffcc00;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ff9900;
        font-size: 13px;
        text-align: center;
        margin-top: 8px;
        margin-bottom: 15px;
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

# --- PANTALLA DE ACCESO Y REGISTRO ---
if not st.session_state.autenticado:

  if st.session_state.modo_pantalla == "registro_completado":
    st.markdown(
        """
        <div class="notice-box">
            <h2>📩 Solicitud enviada con éxito</h2>
            <p>Tiene que esperar hasta que se le autorice la cuenta.</p>
            <p>Cuando tenga autorizada o no autorizada la cuenta, se le mandará un Gmail, por favor, esté atento al Gmail.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("⬅️ Volver al Inicio de Sesión"):
      st.session_state.modo_pantalla = "login"
      st.rerun()

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
          st.error(
              "Lo sentimos mucho, pero esta cuenta no se puede utilizar. Elija"
              " otro Gmail."
          )
        elif reg_user == ADMIN_USER or reg_user in db_usuarios:
          st.error("Ese nombre de usuario ya está ocupado. Elija otro.")
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
    with col_reg2:
      if st.button("Cancelar y volver"):
        st.session_state.modo_pantalla = "login"
        st.rerun()

  elif st.session_state.modo_pantalla == "cierre_permanente":
    st.title("Cerrar sesión permanente de cuenta")

    st.markdown(
        """
        <div class="permanent-warning">
            ⚠️ ADVERTENCIA: Cuando cierres sesión con esta cuenta, luego tendrás que esperar 5 días (120 horas) para volver a iniciar sesión con esta cuenta.
        </div>
        """,
        unsafe_allow_html=True,
    )

    perm_gmail = st.text_input("Introduce tu Gmail:", key="perm_gmail")
    perm_user = st.text_input("Introduce tu Nombre de usuario:", key="perm_user")
    perm_pass = st.text_input(
        "Introduce tu Contraseña:", type="password", key="perm_pass"
    )

    st.write("")
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
      if st.button("Cerrar sesión definitivamente", key="btn_ejecutar_cierre"):
        if not perm_gmail or not perm_user or not perm_pass:
          st.warning("Por favor, rellene todos los campos.")
        elif perm_user == ADMIN_USER:
          st.error(
              "La cuenta administradora principal no puede cerrarse"
              " permanentemente."
          )
        elif perm_user in db_usuarios:
          usr_data = db_usuarios[perm_user]
          if (
              usr_data["gmail"] == perm_gmail
              and usr_data["password"] == perm_pass
          ):
            tiempo_bloqueo = datetime.now() + timedelta(hours=120)
            db_usuarios[perm_user]["bloqueo_hasta"] = tiempo_bloqueo.isoformat()
            guardar_usuarios(db_usuarios)
            st.success(
                "Sesión cerrada definitivamente. Esta cuenta ha sido bloqueada"
                " temporalmente por 5 días."
            )
            time.sleep(2)
            st.session_state.modo_pantalla = "login"
            st.rerun()
          else:
            st.error(
                "Los datos introducidos (Gmail, usuario o contraseña) no"
                " coinciden."
            )
        else:
          st.error("El usuario especificado no existe en el sistema.")
    with col_p2:
      if st.button("Cancelar y volver"):
        st.session_state.modo_pantalla = "login"
        st.rerun()

  else:
    st.title("Inicie sesión en esta web")
    st.subheader("Inicio de sesión")

    u_login = st.text_input("Nombre:", key="login_user")
    p_login = st.text_input("Contraseña:", type="password", key="login_pass")

    st.write("")
    if st.button("Iniciar sesión", key="btn_login"):
      if u_login == ADMIN_USER and p_login == ADMIN_PASS:
        st.session_state.autenticado = True
        st.session_state.usuario_actual = ADMIN_USER
        st.success("Acceso concedido como Líder Principal.")
        time.sleep(1)
        st.rerun()
      elif u_login in db_usuarios:
        usr_data = db_usuarios[u_login]

        bloqueo_hasta_str = usr_data.get("bloqueo_hasta")
        if bloqueo_hasta_str:
          tiempo_limite = datetime.fromisoformat(bloqueo_hasta_str)
          if datetime.now() < tiempo_limite:
            tiempo_restante = tiempo_limite - datetime.now()
            horas_restantes = int(tiempo_restante.total_seconds() // 3600)
            minutos_restantes = int(
                (tiempo_restante.total_seconds() % 3600) // 60
            )
            st.error(
                f"⚠️ Cuenta bloqueada por cierre definitivo. Debe esperar"
                f" {horas_restantes} horas y {minutos_restantes} minutos para"
                " volver a iniciar sesión."
            )
            st.stop()
          else:
            usr_data["bloqueo_hasta"] = None
            guardar_usuarios(db_usuarios)

        if usr_data["password"] == p_login:
          if usr_data["estado"] == "AUTORIZADO":
            st.session_state.autenticado = True
            st.session_state.usuario_actual = u_login
            st.success(
                "Está de buena suerte. Su cuenta ha sido autorizada. Ya puede"
                " acceder a esta web."
            )
            time.sleep(1.5)
            st.rerun()
          elif usr_data["estado"] == "RECHAZADO":
            st.error(
                "Lo sentimos mucho, pero su cuenta no ha sido autorizada. Por"
                " favor, inténtelo de nuevo."
            )
          else:
            st.info(
                "Su cuenta está pendiente de revisión por el Administrador."
                " Vuelva a intentarlo más tarde."
            )
        else:
          st.warning("Contraseña incorrecta.")
      else:
        st.error("El usuario no existe. Por favor, cree una cuenta.")

    st.divider()
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
      if st.button("🔗 Crear una cuenta nueva", type="secondary"):
        st.session_state.modo_pantalla = "registro"
        st.rerun()
    with col_btn2:
      if st.button("🔒 Cerrar sesión permanente de cuenta", type="secondary"):
        st.session_state.modo_pantalla = "cierre_permanente"
        st.rerun()

# --- PANTALLA PRINCIPAL DE LA APLICACIÓN ---
else:
  st.markdown(
      """
    <div class="warning-banner">
        ⚠️ ADVERTENCIA: Ten cuidado con la información que revelas de esta web. Está estrictamente prohibido revelar información sobre esta web. Por favor, si revela algún tipo de información de esta web, será sancionado con una inhabilitación permanente de la cuenta.
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.title("📟 Terminal de Transmisión")
  st.caption(f"Sesión iniciada como: `{st.session_state.usuario_actual}`")

  es_lider = st.session_state.usuario_actual == ADMIN_USER

  if es_lider:
    with st.expander("👑 PANEL DE LÍDER", expanded=True):
      tab_pend, tab_aut, tab_no_aut = st.tabs([
          "⏳ Cuentas en proceso de autorización",
          "✅ Cuentas ya autorizadas",
          "❌ Cuentas no autorizadas",
      ])

      with tab_pend:
        pendientes = {
            u: d
            for u, d in db_usuarios.items()
            if d["estado"] == "PENDIENTE" and u != ADMIN_USER
        }
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
                enviar_confirmacion_usuario(
                    data["gmail"], usr, data["password"], "AUTORIZADO"
                )
                st.success(f"{usr} autorizado el {fecha_hoy} y notificado.")
                time.sleep(1)
                st.rerun()
            with c3:
              if st.button(f"❌ No Autorizar", key=f"no_aut_{usr}"):
                db_usuarios[usr]["estado"] = "RECHAZADO"
                guardar_usuarios(db_usuarios)
                enviar_confirmacion_usuario(
                    data["gmail"], usr, data["password"], "RECHAZADO"
                )
                st.error(f"{usr} rechazado y notificado.")
                time.sleep(1)
                st.rerun()
            st.divider()

      with tab_aut:
        autorizadas = {
            u: d for u, d in db_usuarios.items() if d["estado"] == "AUTORIZADO"
        }
        if not autorizadas:
          st.info("No hay cuentas autorizadas.")
        else:
          for usr, data in autorizadas.items():
            c1, c2 = st.columns([3, 1])
            fecha_str = data.get("fecha_autorizacion", "Fecha no registrada")
            with c1:
              st.write(
                  f"👤 **{usr}** (`{data['gmail']}`) — Autorizado el:"
                  f" `{fecha_str}`"
              )
            with c2:
              if usr != ADMIN_USER:
                if st.button(
                    f"🚫 Desautorizar esta cuenta", key=f"desaut_{usr}"
                ):
                  db_usuarios[usr]["estado"] = "RECHAZADO"
                  guardar_usuarios(db_usuarios)
                  st.warning(f"Se ha desautorizado la cuenta {usr}.")
                  time.sleep(1)
                  st.rerun()
              else:
                st.caption("👑 Cuenta Líder Principal")
            st.divider()

      with tab_no_aut:
        no_autorizadas = {
            u: d
            for u, d in db_usuarios.items()
            if d["estado"] == "RECHAZADO" and u != ADMIN_USER
        }
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
                enviar_confirmacion_usuario(
                    data["gmail"], usr, data["password"], "AUTORIZADO"
                )
                st.success(f"{usr} ha sido autorizada el {fecha_hoy}.")
                time.sleep(1)
                st.rerun()
            st.divider()

  st.divider()

  # ==============================================================================
  # 🔐 SISTEMA DE CIFRADO CON CLAVE BASADA EN PALABRAS DE 10+ CARACTERES
  # ==============================================================================
  st.subheader("⚙️ Controles de Operación y Cifrado")

  with st.sidebar:
    st.header("🔑 Llave de Encriptación")
    st.write(
        "Introduce una clave maestra formada por palabras que tengan **mínimo"
        " 10 caracteres cada una** para garantizar máxima seguridad."
    )

    if st.button("🎲 Generar Clave Segura Automática"):
      # Genera una clave aleatoria larga de Fernet dividida en partes de 10+ caracteres
      raw_key = Fernet.generate_key().decode()
      st.session_state["frase_secreta_faccion"] = raw_key
      st.session_state["clave_fernet_activa"] = raw_key
      st.success("¡Clave segura generada y aplicada con éxito!")

    frase_input = st.text_input(
        "Frase o Clave Secreta:",
        value=st.session_state.get("frase_secreta_faccion", ""),
        type="password",
        help=(
            "Cada palabra introducida debe tener al menos 10 caracteres de"
            " longitud."
        ),
    )

    if frase_input:
      valido, mensaje_error = validar_frase_segura(frase_input)
      if valido:
        st.session_state["frase_secreta_faccion"] = frase_input
        # Si es una clave técnica de Fernet (empieza por base64 larga), la acepta directamente; si es frase de palabras, la deriva de forma segura.
        if len(frase_input.strip()) >= 32 and " " not in frase_input.strip():
          st.session_state["clave_fernet_activa"] = frase_input.strip()
        else:
          st.session_state["clave_fernet_activa"] = (
              generar_clave_desde_frase(frase_input)
          )
        st.success("✅ Clave validada y vinculada correctamente.")
      else:
        st.error(mensaje_error)
        if "clave_fernet_activa" in st.session_state:
          del st.session_state["clave_fernet_activa"]

    # ADVERTENCIA ESTRICTA DE SEGURIDAD
    st.markdown(
        """
        <div class="key-warning">
            ⚠️ <b>ADVERTENCIA ESTRICTA:</b> Está totalmente prohibido revelar o filtrar esta clave secreta a personas ajenas a la facción. Si la clave se filtra, la seguridad de todos los mensajes quedará comprometida permanentemente.
        </div>
        """,
        unsafe_allow_html=True,
    )

  tab_cifrar, tab_descifrar = st.tabs(
      ["🔒 Cifrar Mensaje", "🔓 Descifrar Mensaje"]
  )

  with tab_cifrar:
    msg_claro = st.text_area("Mensaje en claro a proteger:")
    if st.button("Cifrar Transmisión"):
      if not msg_claro.strip():
        st.warning("Por favor, introduce un mensaje.")
      elif "clave_fernet_activa" not in st.session_state:
        st.error(
            "Falta definir una clave o frase válida en la barra lateral (cumpliendo"
            " el requisito de 10+ caracteres por palabra)."
        )
      else:
        try:
          f = Fernet(st.session_state["clave_fernet_activa"])
          token_cifrado = f.encrypt(msg_claro.encode()).decode()

          st.success("¡Transmisión cifrada correctamente!")
          st.write("Copia el siguiente código cifrado:")
          st.code(token_cifrado, language="text")
        except Exception as e:
          st.error(f"Error al cifrar: {e}")

  with tab_descifrar:
    msg_cifrado = st.text_area("Introduce el código cifrado recibido:")
    if st.button("Descifrar Transmisión"):
      if not msg_cifrado.strip():
        st.warning("Por favor, introduce el texto cifrado.")
      elif "clave_fernet_activa" not in st.session_state:
        st.error(
            "Falta definir la clave o frase válida en la barra lateral para"
            " poder leer el mensaje."
        )
      else:
        try:
          f = Fernet(st.session_state["clave_fernet_activa"])
          mensaje_descifrado = f.decrypt(msg_cifrado.encode().strip()).decode()
          st.success("¡Mensaje descifrado con éxito!")
          st.markdown(f"**Mensaje original:** `{mensaje_descifrado}`")
        except Exception:
          st.error(
              "Error crítico: La clave secreta es incorrecta, no cumple con los"
              " requisitos o el mensaje ha sido alterado."
          )

  st.divider()
  if st.button("Cerrar Sesión"):
    st.session_state.autenticado = False
    st.session_state.usuario_actual = ""
    st.session_state.modo_pantalla = "login"
    st.rerun()
