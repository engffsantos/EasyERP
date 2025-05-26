# tests/unit/core/test_auth_flow.py
import pytest
from unittest.mock import patch
from app.core.models.user import User
from app.extensions import db

# Assume fixtures for app context and test client are in conftest.py

def test_register_user_sends_confirmation_email(client, app):
    """Testa se o e-mail de confirmação é enviado no cadastro."""
    with patch("app.shared.utils.email_sender.send_confirmation_email") as mock_send_email:
        response = client.post("/auth/register", data={
            "nome": "Test User Confirm",
            "email": "testconfirm@example.com",
            "senha": "password123",
            "perfil_id": 1 # Placeholder
        }, follow_redirects=True)
        
        assert response.status_code == 200 # Deve redirecionar para login
        assert b"Um e-mail de confirma\xc3\xa7\xc3\xa3o foi enviado" in response.data
        mock_send_email.assert_called_once()
        
        # Verifica se o usuário foi criado no banco como não confirmado
        user = User.query.filter_by(email="testconfirm@example.com").first()
        assert user is not None
        assert not user.email_confirmed
        assert user.confirmation_token is not None

def test_login_unconfirmed_user(client, new_user):
    """Testa o bloqueio de login para usuário não confirmado."""
    new_user.email_confirmed = False
    db.session.add(new_user)
    db.session.commit()
    
    response = client.post("/auth/login", data={
        "email": new_user.email,
        "senha": "testpassword"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"E-mail n\xc3\xa3o confirmado" in response.data
    assert b"Login realizado com sucesso" not in response.data

def test_confirm_email_valid_token(client, new_user):
    """Testa a confirmação de e-mail com token válido."""
    token = new_user.generate_confirmation_token()
    new_user.email_confirmed = False # Garante que começa não confirmado
    db.session.add(new_user)
    db.session.commit()
    
    assert new_user.confirmation_token == token
    
    response = client.get(f"/auth/confirm/{token}", follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Seu e-mail foi confirmado com sucesso" in response.data
    
    # Verifica no banco
    db.session.refresh(new_user)
    assert new_user.email_confirmed is True
    assert new_user.confirmed_at is not None
    assert new_user.confirmation_token is None

def test_confirm_email_invalid_token(client):
    """Testa a confirmação de e-mail com token inválido."""
    response = client.get("/auth/confirm/invalid-token", follow_redirects=True)
    assert response.status_code == 200
    assert b"Link de confirma\xc3\xa7\xc3\xa3o inv\xc3\xa1lido" in response.data

# Adicionar mais testes para outros módulos (Dashboard, Export, Attachments, Audit) conforme necessário
# Exemplo:
# def test_dashboard_access(client, logged_in_user):
#     response = client.get("/dashboard/")
#     assert response.status_code == 200
#     assert b"Dashboard de BI" in response.data

