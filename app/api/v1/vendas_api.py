# app/api/v1/vendas_api.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.vendas.models.cliente import Cliente
from app.vendas.models.oportunidade import Oportunidade
from app.vendas.schemas.oportunidade_schema import cliente_list_schema, oportunidade_list_schema
from app.vendas.viewmodels.opportunity_vm import OpportunityViewModel

vendas_api = Blueprint("vendas_api", __name__, url_prefix="/vendas")


@vendas_api.route("/clientes", methods=["GET"])
@jwt_required()
def listar_clientes():
    clientes = Cliente.query.order_by(Cliente.nome).all()
    return jsonify(cliente_list_schema.dump(clientes)), 200


@vendas_api.route("/oportunidades", methods=["GET"])
@jwt_required()
def listar_oportunidades():
    oportunidades = Oportunidade.query.order_by(Oportunidade.criado_em.desc()).all()
    vms = [OpportunityViewModel.from_model(o) for o in oportunidades]
    return jsonify([vm.__dict__ for vm in vms]), 200
