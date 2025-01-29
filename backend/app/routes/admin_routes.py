from flask import Blueprint, request, jsonify
from ..models import OrderDetail, Product
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """
    Ruta para crear un nuevo producto.

    Solo un administrador puede crear productos. Recibe los datos del producto
    (name, description, price, image_url) y lo guarda en la base de datos.

    Returns:
        jsonify: Respuesta JSON con el resultado de la operación.
    """
    data = request.get_json()

    # Verificar que el usuario es administrador
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'message': 'Permission denied'}), 403

    # Validar datos de entrada
    if not data.get('name') or not data.get('price') or not data.get('image_url'):
        return jsonify({'message': 'Missing required fields'}), 400

    # Crear y agregar el nuevo producto
    new_product = Product(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        image_url=data['image_url']
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully'}), 201

@bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    """
    Ruta para actualizar un producto existente.

    Solo un administrador puede actualizar productos. Recibe los datos del producto
    (name, description, price, image_url) y actualiza los campos correspondientes.

    Returns:
        jsonify: Respuesta JSON con el resultado de la operación.
    """
    data = request.get_json()

    # Verificar que el usuario es administrador
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'message': 'Permission denied'}), 403

    # Buscar el producto por ID
    product = Product.query.get_or_404(id)

    # Actualizar los campos del producto
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'}), 200


@bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'message': 'Permission denied'}), 403

    product = Product.query.get_or_404(id)

    if OrderDetail.query.filter_by(product_id=id).first():
        return jsonify({'message': 'Cannot delete product with associated orders'}), 400

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'}), 200