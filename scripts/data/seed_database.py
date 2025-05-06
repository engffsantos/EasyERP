# scripts/data/seed_database.py

from app import create_app
from app.extensions import db
from app.core.models.profile import Perfil
from app.core.models.permission import Permissao
from app.core.models.user import Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime
import uuid

def seed():
    app = create_app()

    with app.app_context():
        print("🌱 Iniciando seed do banco de dados...")

        db.drop_all()
        db.create_all()

        # Perfis
        admin_profile = Perfil(id=uuid.uuid4(), nome="Administrador", descricao="Acesso total ao sistema")
        financeiro_profile = Perfil(id=uuid.uuid4(), nome="Financeiro", descricao="Acesso ao módulo financeiro")

        db.session.add_all([admin_profile, financeiro_profile])
        db.session.commit()

        # Permissões básicas (exemplos)
        permissoes = [
            Permissao(nome="visualizar_usuarios", descricao="Pode visualizar a lista de usuários"),
            Permissao(nome="gerenciar_financeiro", descricao="Pode gerenciar contas e lançamentos financeiros"),
            Permissao(nome="visualizar_estoque", descricao="Pode visualizar produtos e movimentações de estoque"),
        ]
        db.session.add_all(permissoes)
        db.session.commit()

        # Usuário administrador
        admin = Usuario(
            id=uuid.uuid4(),
            nome="Admin",
            email="admin@easyerp.com",
            senha_hash=generate_password_hash("admin123"),
            perfil_id=admin_profile.id,
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Seed concluído com sucesso.")


if __name__ == "__main__":
    seed()
