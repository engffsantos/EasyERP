# app/estoque/reports/giro_estoque.py

from datetime import datetime
from decimal import Decimal
from sqlalchemy import func, and_
from app.extensions import db
from app.estoque.models.movement import MovimentacaoEstoque
from app.vendas.models.produto import Produto


def gerar_giro_estoque(data_inicio, data_fim):
    """
    Gera um relatório de giro de estoque por produto dentro do intervalo informado.
    """
    data_inicio = datetime.combine(data_inicio, datetime.min.time())
    data_fim = datetime.combine(data_fim, datetime.max.time())

    produtos = Produto.query.order_by(Produto.nome).all()
    relatorio = []

    for produto in produtos:
        total_entradas = db.session.query(func.sum(MovimentacaoEstoque.quantidade)) \
            .filter(
                MovimentacaoEstoque.produto_id == produto.id,
                MovimentacaoEstoque.tipo == 'entrada',
                MovimentacaoEstoque.data_movimentacao >= data_inicio,
                MovimentacaoEstoque.data_movimentacao <= data_fim
            ).scalar() or Decimal(0)

        total_saidas = db.session.query(func.sum(MovimentacaoEstoque.quantidade)) \
            .filter(
                MovimentacaoEstoque.produto_id == produto.id,
                MovimentacaoEstoque.tipo == 'saida',
                MovimentacaoEstoque.data_movimentacao >= data_inicio,
                MovimentacaoEstoque.data_movimentacao <= data_fim
            ).scalar() or Decimal(0)

        total_movimentado = total_entradas + total_saidas

        relatorio.append({
            "produto_id": str(produto.id),
            "nome": produto.nome,
            "total_entradas": float(total_entradas),
            "total_saidas": float(total_saidas),
            "total_movimentado": float(total_movimentado)
        })

    return relatorio
