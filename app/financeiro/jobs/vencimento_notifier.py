# app/financeiro/jobs/vencimento_notifier.py

from datetime import date, timedelta
from app.extensions import db
from app.financeiro.models.transaction import Lancamento
from app.core.models.user import Usuario
from app.core.utils.audit_logger import registrar_acao


def verificar_lancamentos_proximos_vencimento(dias_antecedencia=3):
    """
    Verifica lançamentos com vencimento nos próximos dias e notifica responsáveis.
    """
    hoje = date.today()
    limite = hoje + timedelta(days=dias_antecedencia)

    lancamentos = Lancamento.query.filter(
        Lancamento.data_pagamento.is_(None),
        Lancamento.data_vencimento >= hoje,
        Lancamento.data_vencimento <= limite
    ).all()

    notificacoes = []

    for lancamento in lancamentos:
        usuario = lancamento.usuario
        msg = (
            f"Lançamento '{lancamento.descricao}' de R$ {lancamento.valor:.2f} "
            f"vence em {lancamento.data_vencimento.strftime('%d/%m/%Y')} - Responsável: {usuario.nome} ({usuario.email})"
        )
        registrar_acao("vencimento_proximo", msg, usuario_id=usuario.id)
        notificacoes.append(msg)

    return notificacoes


def notificar_vencimentos():
    """
    Função agendada para rodar diariamente e chamar a verificação de vencimentos.
    """
    notificacoes = verificar_lancamentos_proximos_vencimento()
    for msg in notificacoes:
        print(f"[Notificação Agendada] {msg}")
