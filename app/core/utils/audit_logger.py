# app/core/utils/audit_logger.py

import logging
from datetime import datetime

# Configura o logger específico para auditoria
logger = logging.getLogger("audit")
logger.setLevel(logging.INFO)

# Se nenhum handler foi adicionado, cria um padrão para console
if not logger.hasHandlers():
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[AUDITORIA] [%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def registrar_acao(acao: str, descricao: str, usuario_id: str = None):
    """
    Registra uma ação relevante no log de auditoria.

    :param acao: Nome da ação (ex: 'login_sucesso', 'criar_usuario')
    :param descricao: Descrição detalhada da ação
    :param usuario_id: UUID do usuário que executou a ação (opcional)
    """
    timestamp = datetime.utcnow().isoformat()
    log_msg = f"Ação: {acao} | Usuário: {usuario_id or 'anonimo'} | Detalhes: {descricao}"
    logger.info(log_msg)
