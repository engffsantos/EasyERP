# tests/conftest.py

import pytest
from app import create_app
from app.extensions import db as _db
from sqlalchemy import event
from sqlalchemy.orm import close_all_sessions
from flask_jwt_extended import JWTManager


@pytest.fixture(scope="session")
def app():
    """
    Cria uma instância do app Flask para os testes.
    Usa configuração específica de testes.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-jwt-secret"
    })

    # Inicializa JWT separadamente se necessário
    JWTManager(app)

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    """
    Garante uma sessão de banco de dados limpa para cada teste.
    """
    connection = _db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)

    _db.session = session

    yield _db

    transaction.rollback()
    connection.close()
    session.remove()
    close_all_sessions()


@pytest.fixture(scope="function")
def client(app, db):
    """
    Cliente HTTP de teste.
    """
    return app.test_client()
