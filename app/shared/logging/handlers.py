# app/shared/logging/handlers.py

import logging
from datetime import datetime
from flask_jwt_extended import get_jwt_identity

logger = logging.getLogger(__name__)


def log_acao(usuario_id, acao, detalhes=None):
    """
    Registra uma ação relevante executada por um usuário no sistema.
    """
    logger.info(f"[AÇÃO] Usuário {usuario_id} executou '{acao}' - {detalhes or 'Sem detalhes'}")


def log_erro(mensagem, excecao=None):
    """
    Registra um erro de execução com ou sem exceção.
    """
    if excecao:
        logger.error(f"[ERRO] {mensagem} | Exceção: {str(excecao)}")
    else:
        logger.error(f"[ERRO] {mensagem}")


def log_auditoria(entidade, operacao, usuario_id=None, detalhes=None):
    """
    Log padronizado de auditoria (create/update/delete).
    """
    timestamp = datetime.utcnow().isoformat()
    logger.info(
        f"[AUDITORIA] {operacao.upper()} em {entidade} por usuário {usuario_id or 'desconhecido'} | "
        f"Detalhes: {detalhes or '-'} | {timestamp}"
    )


def log_integracao(sistema, acao, status, payload=None):
    """
    Loga chamadas de integração com sistemas externos (ex: GLPI, ERP, e-mail).
    """
    logger.info(
        f"[INTEGRAÇÃO] {sistema} - {acao} | Status: {status} | Payload: {str(payload)[:500]}"
    )


def log_acao_jwt(acao, detalhes=None):
    """
    Registra ações de usuário autenticado via JWT (sem precisar passar o ID).
    """
    try:
        usuario_id = get_jwt_identity()
    except Exception:
        usuario_id = "desconhecido"
    log_acao(usuario_id, acao, detalhes)
