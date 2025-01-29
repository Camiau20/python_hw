from flask import Flask
from .extensions import db, bcrypt, jwt, migrate  
import os

def create_app():

    """
    Crea y configura la aplicación Flask.

    Esta función crea una instancia de la aplicación Flask, configura las
    variables de entorno, inicializa las extensiones como la base de datos,
    bcrypt para encriptar contraseñas, JWT para autenticación, y Flask-Migrate
    para manejar las migraciones de la base de datos.

    También registra los blueprints necesarios para las rutas de autenticación.

    Returns:
        app: La instancia de la aplicación Flask configurada.
    """
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    return app
