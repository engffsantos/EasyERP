# app/jobs/email_reminder.py

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from app.extensions import db
from app.core.models.user import Usuario

logger = logging.getLogger(__name__)

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USERNAME)


def enviar_lembretes(app):
    """
    Envia lembretes por e-mail para usuários ativos.
    Pode ser personalizado para aniversários, tarefas pendentes, vencimentos, etc.
    """
    with app.app_context():
        try:
            usuarios = Usuario.query.filter_by(ativo=True).all()

            if not usuarios:
                logger.info("Nenhum usuário ativo para envio de lembrete.")
                return

            for usuario in usuarios:
                if not usuario.email:
                    continue

                enviar_email(
                    destinatario=usuario.email,
                    assunto="Lembrete automático - EasyERP",
                    corpo=f"Olá {usuario.nome},\n\nEste é um lembrete automático do sistema EasyERP."
                )
                logger.info(f"Lembrete enviado para: {usuario.email}")

        except Exception as e:
            logger.error(f"Erro ao enviar lembretes: {e}")


def enviar_email(destinatario, assunto, corpo):
    """
    Envia um e-mail com o corpo fornecido.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
