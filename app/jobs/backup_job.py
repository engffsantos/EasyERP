# app/jobs/backup_job.py

import os
import subprocess
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configurações via variáveis de ambiente (.env ou instance/config.py)
DB_NAME = os.getenv("POSTGRES_DB", "easyerp")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")


def executar_backup():
    """
    Executa um backup do banco de dados PostgreSQL usando pg_dump.
    Gera um arquivo .sql datado no diretório definido.
    """
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        data_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{BACKUP_DIR}/backup_{data_str}.sql"

        comando = [
            "pg_dump",
            f"--dbname=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
            "--no-owner",
            "--no-privileges"
        ]

        with open(nome_arquivo, "w") as arquivo:
            subprocess.run(comando, stdout=arquivo, check=True)

        logger.info(f"Backup do banco concluído: {nome_arquivo}")

    except Exception as e:
        logger.error(f"Erro ao executar backup: {e}")
