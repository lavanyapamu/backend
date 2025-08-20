from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from app.main.dto.orders import OrderDTO
from app.main.models.artworks import Artwork
from app.main.models.order_items import OrderItem
from app.main.models.orders import Order
from app.main.services.orders import (
    create_order,
    get_orders_by_user,
    get_order_by_id,
    get_orders_for_artist,
    update_order_status,
    delete_order,
    get_all_orders
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
    
@api.route('/artist-orders/<uuid:artist_id>')
class ArtistOrders(Resource):
    @jwt_required() 
    def get(self, artist_id):
        """
        Get all orders for a given artist
        """
        response, status_code = get_orders_for_artist(artist_id)
        return response, status_code


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
    @jwt_required()
    def put(self, order_id):
        """
        Update overall order status (admin-only).
        """
        identity = get_jwt_identity()
        role = identity.get("role_name", "").lower()
        if role != "admin":
            return {"error": "Unauthorized. Only admin can update overall order status."}, 403

        data = request.get_json()
        if not data or "status" not in data:
            return {"error": "Missing 'status' in request body"}, 400

        return update_order_status(order_id, data["status"])
    
@api.route('/all')
class AllOrders(Resource):
    def get(self):
        limit = request.args.get('limit', type=int)
        orders, status = get_all_orders()
        if isinstance(orders, list) and limit:
            orders = orders[:limit]
        return orders, status

