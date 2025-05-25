# app/shared/utils/email_sender.py
from flask import current_app, render_template, url_for
from flask_mail import Message
from threading import Thread
from app.extensions import mail
from datetime import datetime

def send_async_email(app, msg):
    """Função para enviar e-mail em uma thread separada."""
    with app.app_context():
        try:
            mail.send(msg)
            current_app.logger.info(f"E-mail enviado para {msg.recipients}")
        except Exception as e:
            current_app.logger.error(f"Falha ao enviar e-mail para {msg.recipients}: {e}")

def send_email(to, subject, template, **kwargs):
    """Envia um e-mail usando Flask-Mail de forma assíncrona."""
    app = current_app._get_current_object()
    msg = Message(
        subject,
        sender=app.config["MAIL_DEFAULT_SENDER"],
        recipients=[to]
    )
    # Renderiza o corpo do e-mail a partir de um template HTML
    msg.html = render_template(template + ".html", **kwargs, current_year=datetime.utcnow().year)
    # Envia o e-mail em uma thread separada para não bloquear a requisição
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_confirmation_email(user):
    """Envia o e-mail de confirmação para um novo usuário."""
    token = user.generate_confirmation_token()
    # Gera a URL de confirmação absoluta
    confirmation_url = url_for("core_auth.confirm_email", token=token, _external=True)
    send_email(
        user.email,
        "Confirme seu endereço de e-mail - EasyERP",
        "core/templates/email/confirm_email", # Caminho relativo dentro da pasta templates
        user=user,
        confirmation_url=confirmation_url
    )
