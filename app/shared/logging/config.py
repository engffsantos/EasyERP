# app/shared/logging/config.py

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"
LOG_FILE = os.getenv("LOG_FILE", "logs/easyerp.log")


def configurar_logging(app=None):
    """
    Configura o sistema de logging para a aplicação EasyERP.

    Pode ser usado com ou sem Flask app.
    """
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATEFMT)

    # Cria logger raiz
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # Evita adicionar múltiplos handlers ao reinicializar o app
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (com fallback para criação do diretório)
        try:
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Não foi possível criar handler de arquivo: {e}")

    if app:
        app.logger.handlers = logger.handlers
        app.logger.setLevel(logger.level)
def configure_logging(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")
    log_file = app.config.get("LOG_FILE", "logs/easyerp.log")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    file_handler = RotatingFileHandler(log_file, maxBytes=1024000, backupCount=3)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)

    app.logger.info("Logging configurado com sucesso.")