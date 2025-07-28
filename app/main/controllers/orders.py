from flask import request
from flask_restx import Resource
from app.main.dto.orders import OrderDTO
from app.main.services.orders import (
    create_order,
    get_orders_by_user,
    get_order_by_id,
    update_order_status,
    delete_order
)

api = OrderDTO.api

@api.route('/')
class OrderList(Resource):
    def post(self):
        data = request.get_json()
        return create_order(
            user_id=data['user_id'],
            total_price=data['total_price']
        )

@api.route('/user/<uuid:user_id>')
class UserOrders(Resource):
    def get(self, user_id):
        return get_orders_by_user(user_id)

@api.route('/<uuid:order_id>')
class OrderDetail(Resource):
    def get(self, order_id):
        user_id = request.args.get('user_id')
        return get_order_by_id(order_id, user_id)

    def delete(self, order_id):
        user_id = request.args.get('user_id')
        return delete_order(order_id, user_id)

@api.route('/<uuid:order_id>/status')
class OrderStatus(Resource):
    def put(self, order_id):
        data = request.get_json()
        return update_order_status(order_id, data['status'])
