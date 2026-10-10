import smtplib
from email.mime.text import MIMEText

def send_email(report, email_to):
    msg = MIMEText(report)
    msg["Subject"] = "Reporte diario de acciones"
    msg["From"] = "bot@stockmonitor.com"
    msg["To"] = email_to

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        # Si usas Gmail, debes poner tu App Password aquí
        server.login("TU_CORREO", "TU_APP_PASSWORD")
        server.sendmail("TU_CORREO", email_to, msg.as_string())
