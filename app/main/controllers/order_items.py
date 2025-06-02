from flask import request
from flask_restx import Resource
from app.main.services.order_items import (
    create_order_item, get_order_items_by_order, delete_order_item
)
from app.main.dto.order_items import OrderItemDTO

api = OrderItemDTO.api

@api.route('/<int:order_id>')
class OrderItemsByOrder(Resource):
    def get(self, order_id):
        """Get all items for a specific order"""
        return get_order_items_by_order(order_id)

@api.route('/')
class OrderItemCreate(Resource):
    def post(self):
        """Create a new order item"""
        data = request.get_json()
        return create_order_item(
            data.get('order_id'),
            data.get('artwork_id'),
            data.get('quantity'),
            data.get('price')
        )

@api.route('/item/<int:order_item_id>')
class OrderItemDelete(Resource):
    def delete(self, order_item_id):
        """Delete an order item by ID"""
        return delete_order_item(order_item_id)
