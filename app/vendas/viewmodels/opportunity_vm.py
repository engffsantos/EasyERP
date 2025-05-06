# app/vendas/viewmodels/opportunity_vm.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal


@dataclass
class OpportunityViewModel:
    id: str
    titulo: str
    descricao: Optional[str]
    valor_estimado: float
    status: str
    probabilidade: int
    cliente_nome: str
    cliente_empresa: Optional[str]
    responsavel_nome: str
    criado_em: str
    atualizado_em: str

    @staticmethod
    def from_model(oportunidade):
        """
        Constrói a ViewModel a partir de uma instância de Oportunidade.
        """
        return OpportunityViewModel(
            id=str(oportunidade.id),
            titulo=oportunidade.titulo,
            descricao=oportunidade.descricao,
            valor_estimado=float(oportunidade.valor_estimado or Decimal(0)),
            status=oportunidade.status,
            probabilidade=oportunidade.probabilidade,
            cliente_nome=oportunidade.cliente.nome if oportunidade.cliente else "N/A",
            cliente_empresa=oportunidade.cliente.empresa if oportunidade.cliente else None,
            responsavel_nome=oportunidade.usuario.nome if oportunidade.usuario else "Desconhecido",
            criado_em=oportunidade.criado_em.strftime("%d/%m/%Y %H:%M"),
            atualizado_em=oportunidade.atualizado_em.strftime("%d/%m/%Y %H:%M"),
        )
