# controllers/cart_controller.py

from flask import request
from flask_restx import Resource
from dto.cart import CartDTO
from services import cart_service

api = CartDTO.api
cart_request = CartDTO.cart_request
cart_response = CartDTO.cart_response

@api.route('/')
class CartList(Resource):
    @api.expect(cart_request)
    @api.marshal_with(cart_response, code=201)
    def post(self):
        """Add an item to the cart"""
        data = request.json
        item = cart_service.add_to_cart(data)
        return item.to_dict(), 201

@api.route('/user/<string:user_id>')
class UserCart(Resource):
    @api.marshal_list_with(cart_response)
    def get(self, user_id):
        """Get all cart items for a user"""
        items = cart_service.get_cart_items_by_user(user_id)
        return [item.to_dict() for item in items]

    def delete(self, user_id):
        """Clear entire cart for a user"""
        if cart_service.clear_cart_for_user(user_id):
            return {"message": "Cart cleared successfully"}, 200
        return {"message": "Failed to clear cart"}, 400

@api.route('/<int:cart_id>')
class CartItem(Resource):
    def delete(self, cart_id):
        """Delete a cart item by ID"""
        if cart_service.delete_cart_item(cart_id):
            return {"message": "Item deleted successfully"}, 200
        return {"message": "Item not found"}, 404
