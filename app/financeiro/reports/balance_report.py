# app/financeiro/reports/balance_report.py

from decimal import Decimal
from sqlalchemy import func
from app.extensions import db
from app.financeiro.models.account import Conta
from app.financeiro.models.transaction import Lancamento


def gerar_relatorio_saldos():
    """
    Gera um relatório simples de saldos por conta, incluindo:
    - saldo inicial
    - receitas pagas
    - despesas pagas
    - saldo final (teórico)
    """

    contas = Conta.query.order_by(Conta.nome).all()
    relatorio = []

    for conta in contas:
        receitas = db.session.query(func.sum(Lancamento.valor)) \
            .filter_by(conta_id=conta.id, tipo="receita") \
            .filter(Lancamento.data_pagamento != None) \
            .scalar() or Decimal(0)

        despesas = db.session.query(func.sum(Lancamento.valor)) \
            .filter_by(conta_id=conta.id, tipo="despesa") \
            .filter(Lancamento.data_pagamento != None) \
            .scalar() or Decimal(0)

        saldo_teorico = conta.saldo_inicial + receitas - despesas

        relatorio.append({
            "conta_id": str(conta.id),
            "nome": conta.nome,
            "banco": conta.banco,
            "saldo_inicial": float(conta.saldo_inicial),
            "receitas": float(receitas),
            "despesas": float(despesas),
            "saldo_teorico": float(saldo_teorico),
            "saldo_atual": float(conta.saldo_atual),
            "diferenca": float(conta.saldo_atual - saldo_teorico),
        })

    return relatorio
