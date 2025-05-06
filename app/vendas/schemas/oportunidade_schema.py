# app/vendas/schemas/oportunidade_schema.py

from marshmallow import fields, validate
from app.extensions import ma
from app.vendas.models.cliente import Cliente
from app.vendas.models.oportunidade import Oportunidade


# -------------------- ClienteSchema --------------------

class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True)
    email = ma.auto_field()
    telefone = ma.auto_field()
    empresa = ma.auto_field()

    criado_em = ma.auto_field(dump_only=True)
    atualizado_em = ma.auto_field(dump_only=True)


cliente_schema = ClienteSchema()
cliente_list_schema = ClienteSchema(many=True)


# -------------------- OportunidadeSchema --------------------

class OportunidadeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Oportunidade
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    titulo = ma.auto_field(required=True)
    descricao = ma.auto_field()
    valor_estimado = ma.auto_field(required=True)
    status = ma.auto_field(required=True, validate=validate.OneOf(["aberta", "em negociação", "ganha", "perdida"]))
    probabilidade = ma.auto_field(required=True, validate=validate.Range(min=0, max=100))

    cliente_id = ma.auto_field(required=True)
    usuario_responsavel = ma.auto_field(dump_only=True)

    criado_em = ma.auto_field(dump_only=True)
    atualizado_em = ma.auto_field(dump_only=True)


oportunidade_schema = OportunidadeSchema()
oportunidade_list_schema = OportunidadeSchema(many=True)
