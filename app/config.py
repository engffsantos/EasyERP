# app/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações base (comuns a todos os ambientes)"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-default-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_EXPIRES_MINUTES", 30)))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True

    # Diretório de uploads, se necessário
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")

    # Configurações Flask-Mail (usar variáveis de ambiente em produção)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.mailtrap.io") # Ex: smtp.googlemail.com
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 2525)) # Ex: 587
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "1", "t"]
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() in ["true", "1", "t"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "seu_usuario_mailtrap") # Ex: seu_email@gmail.com
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "sua_senha_mailtrap") # Ex: sua_senha_app
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "EasyERP <noreply@easyerp.com>")


class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:123@127.0.0.1:5432/easyerp"
    )


class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://usuario:senha@localhost:5432/easyerp_prod"
    )


class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///:memory:"
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)


# Dicionário de mapeamento de ambientes
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
