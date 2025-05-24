# app/admin/routes/audit_routes.py
from flask import Blueprint
from app.admin.controllers.audit_controller import AuditController
# Adicionar decorador de autenticação/autorização aqui (ex: @login_required, @admin_required)

# Criação do blueprint para a área administrativa de auditoria
admin_audit_bp = Blueprint("admin_audit", __name__, url_prefix="/admin/audit")

# Rota para listar os logs de auditoria
# Proteger esta rota para que apenas administradores possam acessá-la
@admin_audit_bp.route("/logs", methods=["GET"])
# @admin_required # Descomentar quando a autenticação/autorização estiver implementada
def list_logs():
    return AuditController.list_audit_logs()

def init_app(app):
    """Inicializa o módulo de auditoria administrativa na aplicação Flask"""
    app.register_blueprint(admin_audit_bp)
