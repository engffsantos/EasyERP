# app/financeiro/controllers/account_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.financeiro.models.account import Conta
from app.financeiro.schemas.transaction_schema import conta_schema, conta_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("contas", __name__, url_prefix="/contas")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_contas():
    contas = Conta.query.all()
    return jsonify(conta_list_schema.dump(contas)), 200


@bp.route("/<uuid:conta_id>", methods=["GET"])
@jwt_required()
def obter_conta(conta_id):
    conta = Conta.query.get_or_404(conta_id)
    return jsonify(conta_schema.dump(conta)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_conta():
    dados = request.get_json()
    errors = conta_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    conta = conta_schema.load(dados)
    db.session.add(conta)
    db.session.commit()

    registrar_acao("criar_conta", f"Conta '{conta.nome}' criada.")
    return jsonify(conta_schema.dump(conta)), 201


@bp.route("/<uuid:conta_id>", methods=["PUT"])
@jwt_required()
def atualizar_conta(conta_id):
    conta = Conta.query.get_or_404(conta_id)
    dados = request.get_json()

    for campo in ['nome', 'tipo', 'banco', 'saldo_inicial', 'saldo_atual']:
        if campo in dados:
            setattr(conta, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_conta", f"Conta '{conta.nome}' atualizada.")
    return jsonify(conta_schema.dump(conta)), 200


@bp.route("/<uuid:conta_id>", methods=["DELETE"])
@jwt_required()
def excluir_conta(conta_id):
    conta = Conta.query.get_or_404(conta_id)
    db.session.delete(conta)
    db.session.commit()
    registrar_acao("remover_conta", f"Conta '{conta.nome}' removida.")
    return jsonify({"mensagem": "Conta removida com sucesso."}), 200
