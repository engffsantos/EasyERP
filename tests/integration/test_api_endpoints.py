# tests/integration/test_api_endpoints.py

import pytest
from app.core.models.user import Usuario
from app.core.models.profile import Perfil
from app.extensions import db
from flask import url_for
from werkzeug.security import generate_password_hash


@pytest.fixture
def usuario_cliente():
    perfil = Perfil(nome="Padrão", descricao="Perfil básico")
    db.session.add(perfil)
    db.session.commit()

    usuario = Usuario(
        nome="Teste Integração",
        email="teste@easyerp.com",
        senha_hash=generate_password_hash("senha123"),
        perfil_id=perfil.id
    )
    db.session.add(usuario)
    db.session.commit()
    return usuario


def obter_token_de_acesso(client, email, senha):
    resposta = client.post("/api/v1/login", json={
        "email": email,
        "senha": senha
    })
    dados = resposta.get_json()
    return dados["access_token"] if "access_token" in dados else None


def test_login_funciona(client, usuario_cliente):
    resposta = client.post("/api/v1/login", json={
        "email": usuario_cliente.email,
        "senha": "senha123"
    })
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert "access_token" in dados
    assert dados["usuario"]["email"] == usuario_cliente.email


def test_endpoint_me(client, usuario_cliente):
    token = obter_token_de_acesso(client, usuario_cliente.email, "senha123")
    headers = {"Authorization": f"Bearer {token}"}

    resposta = client.get("/api/v1/me", headers=headers)
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados["email"] == usuario_cliente.email


def test_endpoint_check_token(client, usuario_cliente):
    token = obter_token_de_acesso(client, usuario_cliente.email, "senha123")
    headers = {"Authorization": f"Bearer {token}"}

    resposta = client.get("/api/v1/check", headers=headers)
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "válido"
