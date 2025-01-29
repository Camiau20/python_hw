import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from backend.app import create_app
from backend.app.extensions import db
from flask import render_template
from sqlalchemy.sql import text
from backend.app.models import User

app = create_app()

with app.app_context():
    """
    Inicia un contexto de aplicación para interactuar con la base de datos.

    El contexto de la aplicación es necesario para realizar operaciones
    con la base de datos, como ejecutar una consulta simple para verificar
    la conexión con la base de datos.

    Dentro del contexto, se ejecuta una consulta para probar la conexión
    a la base de datos y luego se crea toda la base de datos si no existe.
    """
    try:
        with db.engine.connect() as connection:
            print("Inicio del contexto de la aplicación")
            result = connection.execute(text('SELECT 1'))
            print("Conexión exitosa a la base de datos.")
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")

    db.create_all()  # Crea todas las tablas de la base de datos si no existen

@app.route('/')
def home():
    """
    Ruta principal para la página de inicio.

    Verifica si ya existe un usuario en la base de datos. Si es así, muestra
    la página de inicio sin el botón de registro. Si no hay usuarios, muestra
    la página de inicio con el botón de registro visible.

    Returns:
        render_template: Renderiza la plantilla 'home.html' con el parámetro
        'show_register' para controlar la visibilidad del botón de registro.
    """
    user_exists = User.query.first()  # Consulta el primer usuario
    if user_exists:
        return render_template('home.html', show_register=False)
    else:
        return render_template('home.html', show_register=True)

@app.route('/register')
def register():
    """
    Ruta para la página de registro.

    Esta página aún no está implementada, pero se define como una ruta
    para mostrar un mensaje indicando que es la página de registro.

    Returns:
        str: Texto indicando que es la página de registro.
    """
    return 'Register Page'

@app.route('/login')
def login():
    """
    Ruta para la página de inicio de sesión.

    Esta página aún no está implementada, pero se define como una ruta
    para mostrar un mensaje indicando que es la página de inicio de sesión.

    Returns:
        str: Texto indicando que es la página de inicio de sesión.
    """
    return 'Login Page'

if __name__ == '__main__':
    """
    Inicia el servidor de la aplicación Flask.

    Se ejecuta la aplicación Flask en el host '0.0.0.0' y en el puerto
    5000. El parámetro 'debug=True' permite que Flask reinicie automáticamente
    el servidor durante el desarrollo cuando se detectan cambios en el código.

    Returns:
        app.run: Inicia la aplicación Flask.
    """
    app.run(host='localhost', port=5000, debug=True)
