# app/core/services/auth_service.py

from datetime import datetime
from app.core.models.user import Usuario
from app.core.utils.audit_logger import registrar_acao
from app.extensions import db


def registrar_login_sucesso(usuario: Usuario):
    """
    Registra no log o login bem-sucedido de um usuário.
    """
    mensagem = f"Login realizado com sucesso para o usuário {usuario.email}"
    registrar_acao("login_sucesso", mensagem, usuario_id=usuario.id)


def registrar_login_falha(email: str):
    """
    Registra no log uma tentativa de login falha.
    """
    mensagem = f"Tentativa de login falha para o e-mail: {email}"
    registrar_acao("login_falha", mensagem, usuario_id=None)
