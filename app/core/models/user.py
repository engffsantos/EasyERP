# app/core/models/user.py

import uuid
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref
from flask import current_app
from itsdangerous import URLSafeTimedSerializer

from app.extensions import db


class User(db.Model): # Renomeado de Usuario para User para consistência
    __tablename__ = "users" # Nome da tabela geralmente é plural

    id = db.Column(db.Integer, primary_key=True) # Alterado para Integer
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfis.id"), nullable=False) # Alterado para Integer
    perfil = db.relationship("Perfil", backref=backref("users", lazy=True))

    supervisor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True) # Alterado para Integer
    supervisor = db.relationship("User", remote_side=[id], backref="subordinados", lazy=True)

    ativo = db.Column(db.Boolean, default=True, nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    confirmation_token = db.Column(db.String(255), nullable=True, unique=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def generate_confirmation_token(self, expiration=3600):
        """Gera um token de confirmação seguro."""
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        self.confirmation_token = s.dumps(self.email, salt="email-confirmation-salt")
        return self.confirmation_token

    def confirm_email(self, token):
        """Verifica o token de confirmação e marca o e-mail como confirmado."""
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            email = s.loads(
                token, 
                salt="email-confirmation-salt", 
                max_age=3600 # Token válido por 1 hora
            )
        except Exception as e:
            current_app.logger.warning(f"Falha ao decodificar token de confirmação: {e}")
            return False
        
        if email != self.email or self.confirmation_token != token:
            current_app.logger.warning(f"Token inválido ou não corresponde ao usuário: {self.email}")
            return False
            
        self.email_confirmed = True
        self.confirmed_at = datetime.utcnow()
        self.confirmation_token = None # Limpa o token após confirmação
        db.session.add(self)
        return True

    def __repr__(self):
        return f"<User {self.nome} - {self.email}>"
