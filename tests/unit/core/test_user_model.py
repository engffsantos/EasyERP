# tests/unit/core/test_user_model.py

import pytest
from datetime import datetime
from app.core.models.user import Usuario
from app.core.models.profile import Perfil
from app.extensions import db


@pytest.fixture
def perfil_padrao():
    perfil = Perfil(nome="Administrador", descricao="Perfil administrativo")
    db.session.add(perfil)
    db.session.commit()
    return perfil


def test_criar_usuario(perfil_padrao):
    usuario = Usuario(
        nome="João Teste",
        email="joao@teste.com",
        senha_hash="hash123",
        perfil_id=perfil_padrao.id
    )
    db.session.add(usuario)
    db.session.commit()

    assert usuario.id is not None
    assert usuario.nome == "João Teste"
    assert usuario.email == "joao@teste.com"
    assert usuario.ativo is True
    assert isinstance(usuario.criado_em, datetime)
    assert isinstance(usuario.atualizado_em, datetime)
    assert usuario.perfil_id == perfil_padrao.id


def test_usuario_supervisor(perfil_padrao):
    supervisor = Usuario(
        nome="Supervisor",
        email="sup@teste.com",
        senha_hash="hashsup",
        perfil_id=perfil_padrao.id
    )
    db.session.add(supervisor)
    db.session.commit()

    subordinado = Usuario(
        nome="Subordinado",
        email="sub@teste.com",
        senha_hash="hashsub",
        perfil_id=perfil_padrao.id,
        supervisor_id=supervisor.id
    )
    db.session.add(subordinado)
    db.session.commit()

    assert subordinado.supervisor_id == supervisor.id
    assert subordinado.supervisor.nome == "Supervisor"
