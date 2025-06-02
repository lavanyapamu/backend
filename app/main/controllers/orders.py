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
_order = OrderDTO.order
_status_update = OrderDTO.order_status_update

@api.route('/')
class OrderList(Resource):
    @api.doc('create a new order')
    @api.expect(_order, validate=True)
    def post(self):
        data = request.json
        return create_order(user_id=data['user_id'], total_price=data['total_price'])

@api.route('/user/<string:user_id>')
class UserOrders(Resource):
    @api.doc('get all orders for a user')
    def get(self, user_id):
        return get_orders_by_user(user_id)

@api.route('/<int:order_id>')
class OrderDetail(Resource):
    @api.doc('get a specific order by id')
    def get(self, order_id):
        return get_order_by_id(order_id)

    @api.doc('delete a specific order')
    def delete(self, order_id):
        user_id = request.args.get('user_id')  # optional query param
        return delete_order(order_id, user_id)

@api.route('/<int:order_id>/status')
class OrderStatus(Resource):
    @api.doc('update order status')
    @api.expect(_status_update, validate=True)
    def put(self, order_id):
        data = request.json
        return update_order_status(order_id, data['status'])
