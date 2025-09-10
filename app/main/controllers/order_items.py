from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from app.main.dto.order_items import OrderItemDTO
from app.main.services.order_items import (
    create_order_item,
    get_order_items_by_order,
    delete_order_item,
    update_order_item_status
)

api = OrderItemDTO.api

@api.route('/<uuid:order_id>')
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
           
        )

@api.route('/item/<uuid:order_item_id>')
class OrderItemDelete(Resource):
    def delete(self, order_item_id):
        return delete_order_item(order_item_id)


@api.route('/items/<uuid:order_item_id>/status')
class OrderItemStatus(Resource):
    @jwt_required()
    def put(self, order_item_id):
        """
        Update a single order item's status.
        Automatically updates overall order status.
        """
        data = request.get_json()
        if not data or "status" not in data:
            return {"error": "Missing 'status' in request body"}, 400

        # Call service with the new status
        return update_order_item_status(order_item_id, data["status"])
