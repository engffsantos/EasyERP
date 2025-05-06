# app/financeiro/models/transaction.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db

# Importações necessárias para os relacionamentos
from app.financeiro.models.categoria_financeira import CategoriaFinanceira
from app.financeiro.models.account import Conta
from app.core.models.user import Usuario


class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(NUMERIC(12, 2), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' ou 'despesa'
    recorrente = db.Column(db.Boolean, default=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    codigo_barras = db.Column(db.String(255), nullable=True)
    nota_fiscal = db.Column(db.String(255), nullable=True)

    categoria_id = db.Column(UUID(as_uuid=True), db.ForeignKey("categorias_financeiras.id"), nullable=False)
    conta_id = db.Column(UUID(as_uuid=True), db.ForeignKey("contas.id"), nullable=False)
    usuario_id = db.Column(UUID(as_uuid=True), db.ForeignKey("usuarios.id"), nullable=False)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    categoria = db.relationship("CategoriaFinanceira", backref="lancamentos", lazy=True)
    conta = db.relationship("Conta", backref="lancamentos", lazy=True)
    usuario = db.relationship("Usuario", backref="lancamentos", lazy=True)

    def __repr__(self):
        return f"<Lancamento {self.descricao} - {self.tipo} - R${self.valor}>"
