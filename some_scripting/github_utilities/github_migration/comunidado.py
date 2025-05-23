import smtplib
from email.message import EmailMessage
import os

# You must create the PASS_APP env variable with your password app.
pass_app = os.environ.get("PASS_APP")

def enviar_mail_mantenimiento(asunto, cuerpo, destinatarios, remitente, contraseña_app):
    # Crear el mensaje
    mensaje = EmailMessage()
    mensaje['Subject'] = asunto
    mensaje['From'] = remitente
    mensaje['To'] = ', '.join(destinatarios)
    mensaje.set_content(cuerpo)

    try:
        # Conexión al servidor SMTP de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contraseña_app)
            smtp.send_message(mensaje)
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Intercambiar la variable "cuerpo" para avisar finalización de tareas.
if __name__ == "__main__":
    asunto = "🚧 Mantenimiento programado"
    cuerpo = """Estimados,
    Algún mail genérico.
Atte.
Los magios."""

    destinatarios = ["", ""]
    remitente = ""
    contraseña_app = pass_app  # Pegá acá tu contraseña de aplicación

    enviar_mail_mantenimiento(asunto, cuerpo, destinatarios, remitente, contraseña_app)
