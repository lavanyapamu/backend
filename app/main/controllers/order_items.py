from flask import request
from flask_restx import Resource
from app.main.dto.order_items import OrderItemDTO
from app.main.services.order_items import (
    create_order_item,
    get_order_items_by_order,
    delete_order_item
)

api = OrderItemDTO.api

@api.route('/<int:order_id>')
class OrderItemsByOrder(Resource):
    def get(self, order_id):
        return get_order_items_by_order(order_id)

@api.route('/')
class OrderItemCreate(Resource):
    def post(self):
        data = request.get_json()
        return create_order_item(
            data.get('order_id'),
            data.get('artwork_id'),
            data.get('quantity'),
            data.get('price')
        )

@api.route('/item/<uuid:order_item_id>')
class OrderItemDelete(Resource):
    def delete(self, order_item_id):
        return delete_order_item(order_item_id)
