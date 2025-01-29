from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from dotenv import load_dotenv


load_dotenv()


def init_app(app):
    """
    Función para inicializar las extensiones y configurar el pool de conexiones.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración del pool de conexiones
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

    db = SQLAlchemy()
    bcrypt = Bcrypt()
    jwt = JWTManager()
    migrate = Migrate()



# Obtener la URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("❌ ERROR: La variable DATABASE_URL no está definida. Verifica tu archivo .env.")
