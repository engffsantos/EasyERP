# app/financeiro/services/reconciliation_service.py

from decimal import Decimal
from app.financeiro.models.account import Conta
from app.financeiro.models.transaction import Lancamento
from app.extensions import db
from sqlalchemy import func


def calcular_saldo_teorico(conta_id):
    """
    Calcula o saldo teórico da conta com base nos lançamentos pagos.
    """
    receitas = db.session.query(func.sum(Lancamento.valor)) \
        .filter_by(conta_id=conta_id, tipo='receita') \
        .filter(Lancamento.data_pagamento != None) \
        .scalar() or Decimal(0)

    despesas = db.session.query(func.sum(Lancamento.valor)) \
        .filter_by(conta_id=conta_id, tipo='despesa') \
        .filter(Lancamento.data_pagamento != None) \
        .scalar() or Decimal(0)

    conta = Conta.query.get_or_404(conta_id)

    saldo_teorico = conta.saldo_inicial + receitas - despesas
    return saldo_teorico.quantize(Decimal('0.01'))


def conciliar_conta(conta_id):
    """
    Realiza a conciliação da conta bancária, comparando o saldo real com o teórico.
    """
    conta = Conta.query.get_or_404(conta_id)
    saldo_teorico = calcular_saldo_teorico(conta_id)
    diferenca = conta.saldo_atual - saldo_teorico

    conciliado = diferenca == Decimal('0.00')

    return {
        "conta_id": str(conta.id),
        "nome": conta.nome,
        "saldo_inicial": float(conta.saldo_inicial),
        "saldo_atual": float(conta.saldo_atual),
        "saldo_teorico": float(saldo_teorico),
        "diferenca": float(diferenca),
        "conciliado": conciliado
    }
