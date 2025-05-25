# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_mail import Mail

# Instâncias das extensões (serão inicializadas em create_app)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()
mail = Mail() # Adicionada instância do Flask-Mail
