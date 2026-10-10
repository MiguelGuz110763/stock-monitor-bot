import smtplib
from email.message import EmailMessage


def send_email(report, email_to, attachments=None):
    # Configura aquí tu servidor SMTP real
    smtp_server = "smtp.tu_proveedor.com"
    smtp_port = 587
    smtp_user = "TU_USUARIO_SMTP"
    smtp_pass = "TU_PASSWORD_SMTP"

    msg = EmailMessage()
    msg["Subject"] = "Reporte de acciones"
    msg["From"] = smtp_user
    msg["To"] = email_to
    msg.set_content(report)

    if attachments:
        for path in attachments:
            with open(path, "rb") as f:
                data = f.read()
            filename = path.split("/")[-1]
            msg.add_attachment(
                data,
                maintype="application",
                subtype="octet-stream",
                filename=filename,
            )

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
