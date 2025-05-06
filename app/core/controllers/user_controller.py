# app/core/controllers/user_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.core.models.user import Usuario
from app.core.models.profile import Perfil
from app.core.schemas.user_schema import usuario_schema, usuario_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_usuarios():
    """
    Lista todos os usuários ativos.
    """
    usuarios = Usuario.query.filter_by(ativo=True).all()
    return jsonify(usuario_list_schema.dump(usuarios)), 200


@bp.route("/<uuid:usuario_id>", methods=["GET"])
@jwt_required()
def obter_usuario(usuario_id):
    """
    Obtém os dados de um usuário específico.
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify(usuario_schema.dump(usuario)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_usuario():
    """
    Cria um novo usuário.
    """
    dados = request.get_json()
    errors = usuario_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    try:
        novo_usuario = usuario_schema.load(dados)
        db.session.add(novo_usuario)
        db.session.commit()

        registrar_acao("criar_usuario", f"Usuário {novo_usuario.email} criado.")
        return jsonify(usuario_schema.dump(novo_usuario)), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": "Email já cadastrado."}), 400


@bp.route("/<uuid:usuario_id>", methods=["PUT"])
@jwt_required()
def atualizar_usuario(usuario_id):
    """
    Atualiza os dados de um usuário existente.
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    dados = request.get_json()

    for campo in ['nome', 'email', 'perfil_id', 'supervisor_id', 'ativo']:
        if campo in dados:
            setattr(usuario, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_usuario", f"Usuário {usuario.email} atualizado.")
    return jsonify(usuario_schema.dump(usuario)), 200


@bp.route("/<uuid:usuario_id>", methods=["DELETE"])
@jwt_required()
def desativar_usuario(usuario_id):
    """
    Desativa (soft delete) um usuário.
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.ativo = False
    db.session.commit()

    registrar_acao("desativar_usuario", f"Usuário {usuario.email} desativado.")
    return jsonify({"mensagem": "Usuário desativado com sucesso."}), 200
