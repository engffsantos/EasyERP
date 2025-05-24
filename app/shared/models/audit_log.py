# app/shared/models/audit_log.py
from app.extensions import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Pode ser nulo para ações do sistema
    ip_address = db.Column(db.String(45), nullable=True) # IPv4 ou IPv6
    action = db.Column(db.String(100), nullable=False) # Ex: 'login', 'create_ticket', 'update_cliente', 'delete_attachment'
    target_type = db.Column(db.String(50), nullable=True) # Ex: 'Ticket', 'Cliente', 'User'
    target_id = db.Column(db.String(36), nullable=True) # ID do objeto afetado (pode ser int ou uuid)
    details = db.Column(db.Text, nullable=True) # Detalhes adicionais, como dados alterados (JSON)
    
    # Relacionamento com usuário (opcional)
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.timestamp} - {self.user_id} - {self.action}>'
