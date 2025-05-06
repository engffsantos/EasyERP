# app/core/services/user_service.py

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.core.models.user import Usuario
from app.core.utils.audit_logger import registrar_acao


def criar_usuario(data: dict) -> Usuario:
    """
    Cria um novo usuário com hash da senha e registra log.
    """
    senha = data.pop("senha", None)
    if not senha:
        raise ValueError("Senha é obrigatória")

    novo_usuario = Usuario(
        nome=data["nome"],
        email=data["email"],
        senha_hash=generate_password_hash(senha),
        perfil_id=data["perfil_id"],
        supervisor_id=data.get("supervisor_id")
    )

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        registrar_acao("criar_usuario", f"Usuário {novo_usuario.email} criado", usuario_id=novo_usuario.id)
        return novo_usuario
    except IntegrityError:
        db.session.rollback()
        raise ValueError("Email já cadastrado")


def atualizar_usuario(usuario_id, data: dict) -> Usuario:
    """
    Atualiza os dados de um usuário.
    """
    usuario = Usuario.query.get_or_404(usuario_id)

    for campo in ['nome', 'email', 'perfil_id', 'supervisor_id', 'ativo']:
        if campo in data:
            setattr(usuario, campo, data[campo])

    db.session.commit()
    registrar_acao("atualizar_usuario", f"Usuário {usuario.email} atualizado", usuario_id=usuario.id)
    return usuario


def desativar_usuario(usuario_id) -> None:
    """
    Desativa (soft delete) um usuário.
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.ativo = False
    db.session.commit()
    registrar_acao("desativar_usuario", f"Usuário {usuario.email} desativado", usuario_id=usuario.id)
