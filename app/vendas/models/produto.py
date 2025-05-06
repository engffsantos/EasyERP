# app/vendas/models/produto.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco_unitario = db.Column(NUMERIC(12, 2), nullable=False)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Produto {self.nome} - R${self.preco_unitario}>"
