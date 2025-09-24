# app/__init__.py
from flask import Flask
from flask_login import login_manager
from app.extensions import db, login_manager
import base64
from app.routes.recepcion_routes import recepcion_bp


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SECRET_KEY'] = 'supersecreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/hotel-python'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Filtro para imágenes
    @app.template_filter('b64encode')
    def b64encode_filter(data):
        return base64.b64encode(data).decode('utf-8')

    # Importar aquí porque Persona depende de db y app ya debe estar inicializado
    from app.models.models import Persona

    @login_manager.user_loader
    def load_user(user_id):
        return Persona.query.get(int(user_id))

    # Registrar Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.cliente_routes import cliente_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cliente_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(recepcion_bp)

    return app


# Ejecutar app desde run.py
app = create_app()

