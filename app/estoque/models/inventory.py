# app/estoque/models/inventory.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db


class ProdutoEstoque(db.Model):
    __tablename__ = "produtos_estoque"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    produto_id = db.Column(UUID(as_uuid=True), db.ForeignKey("produtos.id"), nullable=False)
    armazem_id = db.Column(UUID(as_uuid=True), db.ForeignKey("armazens.id"), nullable=False)

    quantidade = db.Column(NUMERIC(12, 2), nullable=False, default=0)
    estoque_minimo = db.Column(NUMERIC(12, 2), nullable=False, default=0)
    estoque_maximo = db.Column(NUMERIC(12, 2), nullable=True)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    produto = db.relationship("Produto", backref="estoques", lazy=True)
    armazem = db.relationship("Armazem", backref="estoques", lazy=True)

    def __repr__(self):
        return f"<ProdutoEstoque {self.produto.nome} @ {self.armazem.nome} - Qtd: {self.quantidade}>"
