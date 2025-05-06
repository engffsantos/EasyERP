# app/estoque/controllers/estoque_controller.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.estoque.models.movement import MovimentacaoEstoque
from app.estoque.models.inventory import ProdutoEstoque
from app.estoque.models.armazem import Armazem
from app.vendas.models.produto import Produto
from app.core.utils.audit_logger import registrar_acao
from sqlalchemy.exc import SQLAlchemyError
from decimal import Decimal

bp = Blueprint("estoque", __name__, url_prefix="/estoque")


@bp.route("/saldo/<uuid:produto_id>/<uuid:armazem_id>", methods=["GET"])
@jwt_required()
def consultar_saldo(produto_id, armazem_id):
    estoque = ProdutoEstoque.query.filter_by(produto_id=produto_id, armazem_id=armazem_id).first()
    if not estoque:
        return jsonify({"quantidade": 0.0}), 200
    return jsonify({
        "produto_id": str(produto_id),
        "armazem_id": str(armazem_id),
        "quantidade": float(estoque.quantidade)
    }), 200


@bp.route("/movimentar", methods=["POST"])
@jwt_required()
def movimentar_estoque():
    dados = request.get_json()

    tipo = dados.get("tipo")
    produto_id = dados.get("produto_id")
    quantidade = Decimal(str(dados.get("quantidade", 0)))
    usuario_id = get_jwt_identity()
    motivo = dados.get("motivo", "")
    armazem_origem_id = dados.get("armazem_origem_id")
    armazem_destino_id = dados.get("armazem_destino_id")

    if not tipo or not produto_id or quantidade <= 0:
        return jsonify({"erro": "Dados obrigatórios ausentes ou inválidos."}), 400

    try:
        movimentacao = MovimentacaoEstoque(
            tipo=tipo,
            motivo=motivo,
            produto_id=produto_id,
            quantidade=quantidade,
            armazem_origem_id=armazem_origem_id,
            armazem_destino_id=armazem_destino_id,
            usuario_id=usuario_id
        )
        db.session.add(movimentacao)

        # Atualização de estoque
        def atualizar_estoque(produto_id, armazem_id, delta):
            estoque = ProdutoEstoque.query.filter_by(produto_id=produto_id, armazem_id=armazem_id).first()
            if not estoque:
                estoque = ProdutoEstoque(
                    produto_id=produto_id,
                    armazem_id=armazem_id,
                    quantidade=Decimal(0)
                )
                db.session.add(estoque)
            estoque.quantidade += delta

        if tipo == "entrada":
            atualizar_estoque(produto_id, armazem_destino_id, quantidade)
        elif tipo == "saida":
            atualizar_estoque(produto_id, armazem_origem_id, -quantidade)
        elif tipo == "ajuste":
            atualizar_estoque(produto_id, armazem_destino_id, quantidade)
        elif tipo == "transferencia":
            atualizar_estoque(produto_id, armazem_origem_id, -quantidade)
            atualizar_estoque(produto_id, armazem_destino_id, quantidade)
        else:
            return jsonify({"erro": "Tipo de movimentação inválido."}), 400

        db.session.commit()
        registrar_acao("movimentar_estoque", f"{tipo.capitalize()} de {quantidade} unidade(s).")
        return jsonify({"mensagem": "Movimentação registrada com sucesso."}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500
