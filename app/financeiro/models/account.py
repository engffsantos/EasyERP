# app/financeiro/models/account.py

import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from app.extensions import db


class Conta(db.Model):
    __tablename__ = "contas"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # exemplo: 'corrente', 'poupança'
    banco = db.Column(db.String(100), nullable=False)
    saldo_inicial = db.Column(NUMERIC(12, 2), nullable=False, default=0.00)
    saldo_atual = db.Column(NUMERIC(12, 2), nullable=False, default=0.00)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos futuros (opcional):
    # lancamentos = db.relationship('Lancamento', backref='conta', lazy=True)

    def __repr__(self):
        return f"<Conta {self.nome} - Banco: {self.banco}>"
