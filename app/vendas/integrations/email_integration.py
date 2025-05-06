# app/vendas/integrations/email_integration.py

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "EasyERP CRM")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME)


def enviar_email(destinatario, assunto, corpo, reply_to=None):
    """
    Envia um e-mail simples em texto ou HTML.
    """
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    msg['To'] = destinatario
    if reply_to:
        msg['Reply-To'] = reply_to

    msg.set_content(corpo)
    msg.add_alternative(f"""\
    <html>
      <body>
        {corpo}
      </body>
    </html>
    """, subtype='html')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"E-mail enviado com sucesso para {destinatario}")
            return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
