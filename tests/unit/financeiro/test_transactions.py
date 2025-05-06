# tests/unit/financeiro/test_transactions.py

import pytest
from decimal import Decimal
from datetime import date
from app.financeiro.models.account import Conta
from app.financeiro.models.transaction import Lancamento
from app.extensions import db
from app.core.models.user import Usuario
from app.financeiro.models.categoria import CategoriaFinanceira


@pytest.fixture
def conta_teste():
    conta = Conta(nome="Conta Corrente", tipo="banco", banco="Itaú", saldo_inicial=1000, saldo_atual=1000)
    db.session.add(conta)
    db.session.commit()
    return conta


@pytest.fixture
def categoria_teste():
    categoria = CategoriaFinanceira(nome="Aluguel", tipo="despesa")
    db.session.add(categoria)
    db.session.commit()
    return categoria


@pytest.fixture
def usuario_teste():
    usuario = Usuario(nome="Usuário Financeiro", email="fin@teste.com", senha_hash="hash", perfil_id=None)
    db.session.add(usuario)
    db.session.commit()
    return usuario


def test_criar_lancamento_despesa(conta_teste, categoria_teste, usuario_teste):
    lanc = Lancamento(
        descricao="Pagamento do aluguel",
        valor=Decimal("1500.00"),
        tipo="despesa",
        recorrente=False,
        data_vencimento=date.today(),
        codigo_barras="12345678901234567890",
        nota_fiscal="NF1234",
        categoria_id=categoria_teste.id,
        conta_id=conta_teste.id,
        usuario_id=usuario_teste.id
    )
    db.session.add(lanc)
    db.session.commit()

    assert lanc.id is not None
    assert lanc.tipo == "despesa"
    assert lanc.valor == Decimal("1500.00")
    assert lanc.categoria_id == categoria_teste.id
    assert lanc.conta_id == conta_teste.id
    assert lanc.usuario_id == usuario_teste.id


def test_criar_lancamento_receita(conta_teste, categoria_teste, usuario_teste):
    categoria_teste.tipo = "receita"
    db.session.commit()

    lanc = Lancamento(
        descricao="Recebimento de comissão",
        valor=Decimal("750.00"),
        tipo="receita",
        recorrente=True,
        data_vencimento=date.today(),
        data_pagamento=date.today(),
        categoria_id=categoria_teste.id,
        conta_id=conta_teste.id,
        usuario_id=usuario_teste.id
    )
    db.session.add(lanc)
    db.session.commit()

    assert lanc.tipo == "receita"
    assert lanc.recorrente is True
    assert lanc.data_pagamento is not None
