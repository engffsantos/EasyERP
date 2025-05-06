# app/core/schemas/user_schema.py

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.core.models.user import Usuario
from app.extensions import ma


class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        load_instance = True
        ordered = True

    id = ma.auto_field(dump_only=True)
    nome = ma.auto_field(required=True, validate=validate.Length(min=2))
    email = ma.auto_field(required=True, validate=validate.Email())
    senha_hash = ma.auto_field(load_only=True, required=True, validate=validate.Length(min=6))
    perfil_id = ma.auto_field(required=True)
    supervisor_id = ma.auto_field(allow_none=True)

    ativo = ma.auto_field(dump_only=True)
    criado_em = ma.auto_field(dump_only=True)
    atualizado_em = ma.auto_field(dump_only=True)


# Schema para uso em API (criação e atualização)
usuario_schema = UsuarioSchema()
# Schema para uso em listagens (múltiplos usuários)
usuario_list_schema = UsuarioSchema(many=True)
