# app/core/controllers/profile_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.core.models.profile import Perfil
from app.core.schemas.profile_schema import perfil_schema, perfil_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("perfis", __name__, url_prefix="/perfis")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_perfis():
    """
    Lista todos os perfis ativos.
    """
    perfis = Perfil.query.filter_by(ativo=True).all()
    return jsonify(perfil_list_schema.dump(perfis)), 200


@bp.route("/<uuid:perfil_id>", methods=["GET"])
@jwt_required()
def obter_perfil(perfil_id):
    """
    Retorna os dados de um perfil específico.
    """
    perfil = Perfil.query.get_or_404(perfil_id)
    return jsonify(perfil_schema.dump(perfil)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_perfil():
    """
    Cria um novo perfil.
    """
    dados = request.get_json()
    errors = perfil_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    perfil = perfil_schema.load(dados)
    db.session.add(perfil)
    db.session.commit()

    registrar_acao("criar_perfil", f"Perfil '{perfil.nome}' criado.")
    return jsonify(perfil_schema.dump(perfil)), 201


@bp.route("/<uuid:perfil_id>", methods=["PUT"])
@jwt_required()
def atualizar_perfil(perfil_id):
    """
    Atualiza um perfil existente.
    """
    perfil = Perfil.query.get_or_404(perfil_id)
    dados = request.get_json()

    for campo in ['nome', 'descricao', 'ativo']:
        if campo in dados:
            setattr(perfil, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_perfil", f"Perfil '{perfil.nome}' atualizado.")
    return jsonify(perfil_schema.dump(perfil)), 200


@bp.route("/<uuid:perfil_id>", methods=["DELETE"])
@jwt_required()
def desativar_perfil(perfil_id):
    """
    Desativa um perfil (soft delete).
    """
    perfil = Perfil.query.get_or_404(perfil_id)
    perfil.ativo = False
    db.session.commit()

    registrar_acao("desativar_perfil", f"Perfil '{perfil.nome}' desativado.")
    return jsonify({"mensagem": "Perfil desativado com sucesso."}), 200
