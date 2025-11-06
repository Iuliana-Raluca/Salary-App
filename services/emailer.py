import smtplib
from email.message import EmailMessage
from config import Config

def send_email_with_attachments(to: str, subject: str, body: str, attachments: list[str]):
    msg = EmailMessage()
    msg["From"] = Config.SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    for file_path in attachments:
        with open(file_path, "rb") as f:
            file_data = f.read()
        filename = file_path.split("/")[-1]
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=filename)

    with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(Config.SMTP_USER, Config.SMTP_PASS)
        smtp.send_message(msg)
