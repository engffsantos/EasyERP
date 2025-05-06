# app/financeiro/schemas/transaction_schema.py

from marshmallow import fields, validate
from app.extensions import ma
from app.financeiro.models.account import Conta
from app.financeiro.models.transaction import Lancamento


# --------------------- ContaSchema ---------------------

class ContaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Conta
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True)
    tipo = ma.auto_field(required=True)
    banco = ma.auto_field(required=True)
    saldo_inicial = ma.auto_field(required=True)
    saldo_atual = ma.auto_field(dump_only=True)

    criado_em = ma.auto_field(dump_only=True)
    atualizado_em = ma.auto_field(dump_only=True)


conta_schema = ContaSchema()
conta_list_schema = ContaSchema(many=True)


# --------------------- LancamentoSchema ---------------------

class LancamentoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lancamento
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    descricao = ma.auto_field(required=True)
    valor = ma.auto_field(required=True)
    tipo = ma.auto_field(required=True, validate=validate.OneOf(["receita", "despesa"]))
    recorrente = ma.auto_field()
    data_vencimento = fields.Date(required=True)
    data_pagamento = fields.Date(allow_none=True)
    codigo_barras = ma.auto_field()
    nota_fiscal = ma.auto_field()

    categoria_id = ma.auto_field(required=True)
    conta_id = ma.auto_field(required=True)
    usuario_id = ma.auto_field(dump_only=True)

    criado_em = ma.auto_field(dump_only=True)
    atualizado_em = ma.auto_field(dump_only=True)


lancamento_schema = LancamentoSchema()
lancamento_list_schema = LancamentoSchema(many=True)
