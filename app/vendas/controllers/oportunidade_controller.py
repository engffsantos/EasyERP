# app/vendas/controllers/oportunidade_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.vendas.models.oportunidade import Oportunidade
from app.vendas.schemas.oportunidade_schema import oportunidade_schema, oportunidade_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("oportunidades", __name__, url_prefix="/oportunidades")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_oportunidades():
    oportunidades = Oportunidade.query.order_by(Oportunidade.criado_em.desc()).all()
    return jsonify(oportunidade_list_schema.dump(oportunidades)), 200


@bp.route("/<uuid:oportunidade_id>", methods=["GET"])
@jwt_required()
def obter_oportunidade(oportunidade_id):
    oportunidade = Oportunidade.query.get_or_404(oportunidade_id)
    return jsonify(oportunidade_schema.dump(oportunidade)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_oportunidade():
    dados = request.get_json()
    errors = oportunidade_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    dados["usuario_responsavel"] = get_jwt_identity()
    oportunidade = oportunidade_schema.load(dados)
    db.session.add(oportunidade)
    db.session.commit()

    registrar_acao("criar_oportunidade", f"Oportunidade '{oportunidade.titulo}' criada.")
    return jsonify(oportunidade_schema.dump(oportunidade)), 201


@bp.route("/<uuid:oportunidade_id>", methods=["PUT"])
@jwt_required()
def atualizar_oportunidade(oportunidade_id):
    oportunidade = Oportunidade.query.get_or_404(oportunidade_id)
    dados = request.get_json()

    campos = [
        "titulo", "descricao", "valor_estimado", "status",
        "probabilidade", "cliente_id"
    ]
    for campo in campos:
        if campo in dados:
            setattr(oportunidade, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_oportunidade", f"Oportunidade '{oportunidade.titulo}' atualizada.")
    return jsonify(oportunidade_schema.dump(oportunidade)), 200


@bp.route("/<uuid:oportunidade_id>", methods=["DELETE"])
@jwt_required()
def remover_oportunidade(oportunidade_id):
    oportunidade = Oportunidade.query.get_or_404(oportunidade_id)
    db.session.delete(oportunidade)
    db.session.commit()
    registrar_acao("remover_oportunidade", f"Oportunidade '{oportunidade.titulo}' removida.")
    return jsonify({"mensagem": "Oportunidade removida com sucesso."}), 200
