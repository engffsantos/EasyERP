# app/service_desk/workflows/sla_rules.py

from datetime import timedelta, datetime

# Regras de SLA por prioridade
SLA_PRAZOS = {
    "crítica": timedelta(hours=2),
    "alta": timedelta(hours=8),
    "normal": timedelta(days=1),
    "baixa": timedelta(days=3),
}


def calcular_prazo_limite(criado_em, prioridade):
    """
    Calcula o prazo máximo de atendimento com base na prioridade do ticket.

    :param criado_em: datetime de criação do ticket
    :param prioridade: prioridade do ticket (baixa, normal, alta, crítica)
    :return: datetime limite de atendimento
    """
    prazo = SLA_PRAZOS.get(prioridade.lower(), timedelta(days=1))
    return criado_em + prazo


def verificar_conformidade_sla(criado_em, prioridade, data_atendimento=None):
    """
    Verifica se o ticket foi atendido dentro do prazo de SLA.

    :param criado_em: datetime de criação do ticket
    :param prioridade: prioridade do ticket
    :param data_atendimento: datetime de quando foi atendido (ou None para verificar status atual)
    :return: (bool, datetime limite)
    """
    limite = calcular_prazo_limite(criado_em, prioridade)
    data_verificacao = data_atendimento or datetime.utcnow()
    em_conformidade = data_verificacao <= limite
    return em_conformidade, limite
