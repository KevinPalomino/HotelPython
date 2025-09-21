# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
# Ruta a la que redirige si no ha iniciado sesión
login_manager.login_view = 'auth.login'
