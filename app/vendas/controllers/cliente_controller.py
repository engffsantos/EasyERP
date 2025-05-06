# app/vendas/controllers/cliente_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.vendas.models.cliente import Cliente
from app.vendas.schemas.oportunidade_schema import cliente_schema, cliente_list_schema
from app.core.utils.audit_logger import registrar_acao

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return jsonify(cliente_list_schema.dump(clientes)), 200


@bp.route("/<uuid:cliente_id>", methods=["GET"])
@jwt_required()
def obter_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    return jsonify(cliente_schema.dump(cliente)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def criar_cliente():
    dados = request.get_json()
    errors = cliente_schema.validate(dados)
    if errors:
        return jsonify(errors), 400

    cliente = cliente_schema.load(dados)
    db.session.add(cliente)
    db.session.commit()
    registrar_acao("criar_cliente", f"Cliente '{cliente.nome}' criado.")
    return jsonify(cliente_schema.dump(cliente)), 201


@bp.route("/<uuid:cliente_id>", methods=["PUT"])
@jwt_required()
def atualizar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    dados = request.get_json()

    for campo in ["nome", "email", "telefone", "empresa"]:
        if campo in dados:
            setattr(cliente, campo, dados[campo])

    db.session.commit()
    registrar_acao("atualizar_cliente", f"Cliente '{cliente.nome}' atualizado.")
    return jsonify(cliente_schema.dump(cliente)), 200


@bp.route("/<uuid:cliente_id>", methods=["DELETE"])
@jwt_required()
def remover_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    registrar_acao("remover_cliente", f"Cliente '{cliente.nome}' removido.")
    return jsonify({"mensagem": "Cliente removido com sucesso."}), 200
