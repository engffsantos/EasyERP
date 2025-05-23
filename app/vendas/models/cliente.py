# app/vendas/models/cliente.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.extensions import db
from app.vendas.models.interacao import Interacao


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True) # Alterado para Integer para compatibilidade com Attachment
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(50), nullable=True)
    empresa = db.Column(db.String(255), nullable=True)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos com uso de back_populates
    oportunidades = db.relationship("Oportunidade", back_populates="cliente", lazy=True)
    interacoes = db.relationship("Interacao", backref="cliente", lazy=True)
    
    # Relacionamento com Anexos
    attachments = db.relationship("Attachment", backref="cliente", lazy="dynamic")

    def __repr__(self):
        return f"<Cliente {self.nome}>"
