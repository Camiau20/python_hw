from flask import Blueprint, jsonify
from ..models import Product

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/', methods=['GET'])
def get_all_products():
    """
    Ruta para obtener todos los productos.

    Devuelve una lista con todos los productos almacenados en la base de datos.

    Returns:
        jsonify: Respuesta JSON con la lista de productos.
    """
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url
    } for product in products]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    """
    Ruta para obtener un producto específico.

    Recibe el ID de un producto y devuelve los detalles de ese producto.

    Returns:
        jsonify: Respuesta JSON con los detalles del producto.
    """
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url
    }), 200
