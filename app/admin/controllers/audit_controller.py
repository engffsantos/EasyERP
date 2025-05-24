# app/admin/controllers/audit_controller.py
from flask import render_template, request, current_app
from app.shared.models.audit_log import AuditLog
from app.extensions import db
from sqlalchemy import desc

class AuditController:
    
    @staticmethod
    def list_audit_logs():
        """Exibe a lista de logs de auditoria com paginação e filtros."""
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)
        
        # Filtros (exemplo básico)
        user_filter = request.args.get("user_id")
        action_filter = request.args.get("action")
        target_type_filter = request.args.get("target_type")
        
        query = AuditLog.query
        
        if user_filter:
            query = query.filter(AuditLog.user_id == user_filter)
        if action_filter:
            query = query.filter(AuditLog.action.ilike(f"%{action_filter}%"))
        if target_type_filter:
            query = query.filter(AuditLog.target_type.ilike(f"%{target_type_filter}%"))
            
        # Ordenar pelos mais recentes primeiro
        query = query.order_by(desc(AuditLog.timestamp))
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        logs = pagination.items
        
        return render_template(
            "admin/audit_log.html", 
            logs=logs, 
            pagination=pagination,
            # Passar filtros para manter no formulário
            user_filter=user_filter,
            action_filter=action_filter,
            target_type_filter=target_type_filter
        )
