# instance/config.py

import os

class Config:
    # ==================== Flask ====================
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # ==================== Banco de Dados ====================
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/easyerp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==================== JWT ====================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRES_IN", 3600))  # em segundos

    # ==================== Email ====================
    EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", EMAIL_USERNAME)

    # ==================== Backup ====================
    BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")

    # ==================== Logging ====================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/easyerp.log")

    # ==================== PDF ====================
    WEASYPRINT_BASE_URL = os.getenv("WEASYPRINT_BASE_URL", "http://localhost:5000")

    # ==================== Outras configs ====================
    DEBUG = os.getenv("DEBUG", "False") == "True"
    TESTING = os.getenv("TESTING", "False") == "True"

