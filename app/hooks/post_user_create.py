# app/hooks/post_user_create.py

import logging
from flask import current_app
from app.shared.logging.handlers import log_auditoria
from app.jobs.email_reminder import enviar_email
from app.core.models.user import Usuario

logger = logging.getLogger(__name__)


def acao_pos_criacao_usuario(usuario: Usuario):
    """
    Ação executada logo após a criação de um novo usuário no sistema.
    """
    try:
        # 1. Log de auditoria
        log_auditoria(
            entidade="Usuario",
            operacao="create",
            usuario_id=usuario.id,
            detalhes=f"Usuário {usuario.nome} ({usuario.email}) criado."
        )

        # 2. Envio de e-mail de boas-vindas (se houver e-mail válido)
        if usuario.email:
            assunto = "Bem-vindo ao EasyERP!"
            corpo = f"""
Olá {usuario.nome},

Seu cadastro foi criado com sucesso no sistema EasyERP.

Você já pode acessar com seu e-mail cadastrado. Em caso de dúvidas, entre em contato com o suporte.

Atenciosamente,
Equipe EasyData360
"""
            enviar_email(destinatario=usuario.email, assunto=assunto, corpo=corpo)
            logger.info(f"E-mail de boas-vindas enviado para {usuario.email}")

    except Exception as e:
        logger.error(f"Erro no hook pós-criação de usuário: {e}")
