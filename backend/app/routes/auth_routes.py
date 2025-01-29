from flask import Blueprint, request, jsonify
from ..models import User
from ..extensions import db, bcrypt, jwt
from flask_jwt_extended import create_access_token


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Ruta para registrar un nuevo usuario.

    Recibe los datos de usuario (username, email, password), encripta la
    contraseña y guarda el usuario en la base de datos. Si el usuario ya existe,
    devuelve un mensaje de error.

    Returns:
        jsonify: Respuesta JSON con el resultado de la operación.
    """
    data = request.get_json()

    # Validación de datos de entrada
    if not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({'message': 'Missing required fields'}), 400

    # Verificar si el usuario ya existe
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    # Encriptar la contraseña
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Crear el nuevo usuario
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Si hay un error, deshacer la transacción
        return jsonify({'message': f'Error: {str(e)}'}), 500
    finally:
        db.session.remove()  # Asegúrate de limpiar la sesión

    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    Ruta para iniciar sesión y obtener un token JWT.

    Recibe las credenciales de login (username, password), verifica si son
    correctas y genera un token JWT para el usuario autenticado.

    Returns:
        jsonify: Respuesta JSON con el token JWT.
    """
    data = request.get_json()

    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'is_admin': user.is_admin  
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401
