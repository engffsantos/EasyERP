# app/shared/utils/audit_logger.py
from functools import wraps
from flask import request, g # g para armazenar usuário atual, se aplicável
from app.extensions import db
from app.shared.models.audit_log import AuditLog
import json

def log_audit(action, target_type=None, target_id=None, details=None):
    """Registra um evento de auditoria no banco de dados."""
    try:
        user_id = g.user.id if hasattr(g, 'user') and g.user else None
        ip_address = request.remote_addr
        
        # Converte detalhes para JSON se for um dicionário
        if isinstance(details, dict):
            details_json = json.dumps(details, ensure_ascii=False, default=str) # default=str para lidar com tipos não serializáveis
        else:
            details_json = str(details) if details is not None else None
            
        log_entry = AuditLog(
            user_id=user_id,
            ip_address=ip_address,
            action=action,
            target_type=target_type,
            target_id=str(target_id) if target_id is not None else None, # Garante que seja string
            details=details_json
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Logar o erro de auditoria em um log de sistema separado, se necessário
        print(f"Erro ao registrar log de auditoria: {e}") # Substituir por logger adequado

def audit_log_decorator(action_template, target_type_func=None, target_id_func=None, details_func=None):
    """
    Decorator para registrar automaticamente eventos de auditoria em rotas Flask.

    Args:
        action_template (str): Template para a descrição da ação (pode usar {args} ou {kwargs}).
        target_type_func (callable, optional): Função que recebe args/kwargs da rota e retorna o tipo do alvo.
        target_id_func (callable, optional): Função que recebe args/kwargs da rota e retorna o ID do alvo.
        details_func (callable, optional): Função que recebe args/kwargs da rota e retorna detalhes adicionais.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Executa a função original primeiro
            response = func(*args, **kwargs)
            
            # Tenta registrar o log após a execução bem-sucedida
            # (Pode ser ajustado para registrar antes ou em caso de erro também)
            try:
                action = action_template.format(args=args, kwargs=kwargs)
                target_type = target_type_func(*args, **kwargs) if target_type_func else None
                target_id = target_id_func(*args, **kwargs) if target_id_func else None
                details = details_func(*args, **kwargs) if details_func else None
                
                log_audit(action, target_type, target_id, details)
            except Exception as e:
                # Logar erro na tentativa de auditoria, mas não impedir a resposta original
                print(f"Erro no decorator de auditoria para {func.__name__}: {e}")
                
            return response
        return wrapper
    return decorator
