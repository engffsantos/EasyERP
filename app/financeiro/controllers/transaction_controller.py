# app/financeiro/controllers/transaction_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.financeiro.models.transaction import Lancamento
from app.financeiro.schemas.transaction_schema import lancamento_schema, lancamento_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("lancamentos", __name__, url_prefix="/lancamentos")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_lancamentos():
    lancamentos = Lancamento.query.all()
    return jsonify(lancamento_list_schema.dump(lancamentos)), 200


@bp.route("/<uuid:lancamento_id>", methods=["GET"])
@jwt_required()
def obter_lancamento(lancamento_id):
    lancamento = Lancamento.query.get_or_404(lancamento_id)
    return jsonify(lancamento_schema.dump(lancamento)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_lancamento():
    dados = request.get_json()
    errors = lancamento_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    usuario_id = get_jwt_identity()
    dados["usuario_id"] = usuario_id

    lancamento = lancamento_schema.load(dados)
    db.session.add(lancamento)
    db.session.commit()

    registrar_acao("criar_lancamento", f"Lançamento '{lancamento.descricao}' criado.", usuario_id=usuario_id)
    return jsonify(lancamento_schema.dump(lancamento)), 201


@bp.route("/<uuid:lancamento_id>", methods=["PUT"])
@jwt_required()
def atualizar_lancamento(lancamento_id):
    lancamento = Lancamento.query.get_or_404(lancamento_id)
    dados = request.get_json()

    for campo in ['descricao', 'valor', 'tipo', 'recorrente', 'data_vencimento',
                  'data_pagamento', 'codigo_barras', 'nota_fiscal', 'categoria_id', 'conta_id']:
        if campo in dados:
            setattr(lancamento, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_lancamento", f"Lançamento '{lancamento.descricao}' atualizado.")
    return jsonify(lancamento_schema.dump(lancamento)), 200


@bp.route("/<uuid:lancamento_id>", methods=["DELETE"])
@jwt_required()
def remover_lancamento(lancamento_id):
    lancamento = Lancamento.query.get_or_404(lancamento_id)
    db.session.delete(lancamento)
    db.session.commit()
    registrar_acao("remover_lancamento", f"Lançamento '{lancamento.descricao}' removido.")
    return jsonify({"mensagem": "Lançamento removido com sucesso."}), 200
