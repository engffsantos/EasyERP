# app/core/utils/decorators.py

from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import jsonify, request

from app.core.models.user import Usuario
from app.core.utils.audit_logger import registrar_acao


def requer_permissao(nome_permissao):
    """
    Decorador que verifica se o usuário autenticado possui uma permissão específica.
    """
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            usuario_id = get_jwt_identity()
            usuario = Usuario.query.get(usuario_id)

            if not usuario or not usuario.perfil:
                return jsonify({"erro": "Usuário ou perfil inválido"}), 403

            permissoes = [p.nome for p in usuario.perfil.permissoes]
            if nome_permissao not in permissoes:
                return jsonify({"erro": f"Permissão '{nome_permissao}' negada"}), 403

            return func(*args, **kwargs)
        return decorated_function
    return wrapper


def auditar_acao(acao_nome):
    """
    Decorador que registra automaticamente uma ação de auditoria.
    """
    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            usuario_id = get_jwt_identity()
            resultado = func(*args, **kwargs)
            registrar_acao(acao_nome, f"Ação executada em {request.path}", usuario_id=usuario_id)
            return resultado
        return decorated_function
    return wrapper
