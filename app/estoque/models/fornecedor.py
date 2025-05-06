# app/estoque/models/fornecedor.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db


class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), nullable=True)
    contato = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    compras = db.relationship("Compra", backref="fornecedor", lazy=True)

    def __repr__(self):
        return f"<Fornecedor {self.nome}>"
