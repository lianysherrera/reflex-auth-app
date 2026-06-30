import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

MAILTRAP_HOST = os.getenv("MAILTRAP_HOST", "")
MAILTRAP_PORT = int(os.getenv("MAILTRAP_PORT", "2525"))
MAILTRAP_USERNAME = os.getenv("MAILTRAP_USERNAME", "")
MAILTRAP_PASSWORD = os.getenv("MAILTRAP_PASSWORD", "")

FROM_EMAIL = "no-reply@reflex-auth-app.test"

def send_verification_email(to_email: str, verification_token: str) -> None:
    verification_link = f"http://localhost:3000/verify?token={verification_token}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Verifica tu cuenta - Reflex Auth App"
    message["From"] = FROM_EMAIL
    message["To"] = to_email

    text_body = (
        f"¡Hola!\n\n"
        f"Gracias por registrarte. Verifica tu cuenta haciendo clic en este link:\n"
        f"{verification_link}\n\n"
        f"Si no creaste esta cuenta, puedes ignorar este mensaje."
    )
    html_body = (
        f"<p>¡Hola!</p>"
        f"<p>Gracias por registrarte. Verifica tu cuenta haciendo clic en el siguiente botón:</p>"
        f'<p><a href="{verification_link}">Verificar mi cuenta</a></p>'
        f"<p>Si no creaste esta cuenta, puedes ignorar este mensaje.</p>"
    )

    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
        server.starttls()
        server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, message.as_string())