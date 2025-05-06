from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.core.models.user import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash

user_interface = Blueprint("user_interface", __name__)

DEFAULT_PROFILE_ID = 1

@user_interface.route("/users/novo", methods=["GET", "POST"])
def criar_usuario():
    if request.method == "GET":
        return render_template("core/users/novo.html")

        #return render_template("/app/core/templates/core/users/novo.html"),
    
    return processar_criacao_usuario()

def processar_criacao_usuario():
    dados_usuario = {
        'nome': request.form["nome"],
        'email': request.form["email"],
        'senha': request.form["senha"]
    }
    
    if email_ja_cadastrado(dados_usuario['email']):
        flash("E-mail já cadastrado", "danger")
        return redirect(url_for("user_interface.criar_usuario"))
    
    usuario = criar_novo_usuario(dados_usuario)
    salvar_usuario(usuario)
    
    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for("user_interface.criar_usuario"))

def email_ja_cadastrado(email):
    return Usuario.query.filter_by(email=email).first() is not None

def criar_novo_usuario(dados):
    return Usuario(
        nome=dados['nome'],
        email=dados['email'],
        senha_hash=generate_password_hash(dados['senha']),
        perfil_id=DEFAULT_PROFILE_ID,
        ativo=True
    )

def salvar_usuario(usuario):
    db.session.add(usuario)
    db.session.commit()