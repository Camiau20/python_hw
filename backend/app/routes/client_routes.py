from flask import Blueprint, request, jsonify
from ..models import Order, OrderDetail, Product, User
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity


bp = Blueprint('client', __name__, url_prefix='/client')



@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    orders = Order.query.filter_by(user_id=user.id).all()


    orders_data = []
    for order in orders:
        order_data = {
            'id': order.id,
            'total': order.total,
            'status': order.status,
            'created_at': order.created_at,
            'details': []
        }
        for detail in order.details:
            order_data['details'].append({
                'product_name': detail.product.name,
                'quantity': detail.quantity,
                'price': detail.price
            })
        orders_data.append(order_data)

    return jsonify(orders_data), 200


@bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)


    data = request.get_json()
    if not data.get('products'):
        return jsonify({'message': 'Missing products'}), 400

    total = 0
    order_details = []
    for item in data['products']:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({'message': f'Product {item["product_id"]} not found'}), 404

        total += product.price * item['quantity']
        order_details.append(OrderDetail(
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        ))

    new_order = Order(
        user_id=user.id,
        total=total,
        status='Pending',
        details=order_details
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201