# app/core/schemas/profile_schema.py

from marshmallow import Schema, fields
from app.core.models.profile import Perfil


class PerfilSchema(Schema):
    """
    Schema para serializar e desserializar objetos do modelo Perfil.
    """
    id = fields.UUID(dump_only=True)
    nome = fields.Str(required=True)
    descricao = fields.Str()
    ativo = fields.Bool()
    criado_em = fields.DateTime(dump_only=True)
    atualizado_em = fields.DateTime(dump_only=True)


# Instâncias reutilizáveis
perfil_schema = PerfilSchema()
perfil_list_schema = PerfilSchema(many=True)
