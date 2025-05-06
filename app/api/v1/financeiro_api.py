# app/api/v1/financeiro_api.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.financeiro.models.account import Conta
from app.financeiro.models.transaction import Lancamento
from app.financeiro.schemas.transaction_schema import conta_list_schema, lancamento_list_schema
from app.financeiro.services.reconciliation_service import conciliar_conta
from app.extensions import db

financeiro_api = Blueprint("financeiro_api", __name__, url_prefix="/financeiro")


@financeiro_api.route("/contas", methods=["GET"])
@jwt_required()
def listar_contas():
    contas = Conta.query.order_by(Conta.nome).all()
    return jsonify(conta_list_schema.dump(contas)), 200


@financeiro_api.route("/lancamentos", methods=["GET"])
@jwt_required()
def listar_lancamentos():
    usuario_id = get_jwt_identity()
    lancamentos = Lancamento.query.filter_by(usuario_id=usuario_id).order_by(Lancamento.data_vencimento.desc()).all()
    return jsonify(lancamento_list_schema.dump(lancamentos)), 200


@financeiro_api.route("/contas/<uuid:conta_id>/conciliacao", methods=["GET"])
@jwt_required()
def conciliacao(conta_id):
    try:
        resultado = conciliar_conta(conta_id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
