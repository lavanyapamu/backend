# controllers/cart_controller.py

from flask import request, current_app
from flask_restx import Resource
from app.main.dto.cart import CartDTO
from app.main.services import cart

api = CartDTO.api

@api.route('/')
class CartList(Resource):
    def post(self):
        """Add an item to the cart (stock validated)"""
        data = request.json
        try:
            item = cart.add_to_cart(data)

            # If service returned (dict, status) for errors (e.g., stock)
            if isinstance(item, tuple):
                payload, status = item
                return payload, status

            # Success: return cart item as dict
            return item.to_dict(), 201
        except Exception as e:
            current_app.logger.error(f"Error adding item to cart: {e}")
            api.abort(500, f"Error adding item to cart: {str(e)}")

    def get(self):
        """Get all cart items (Admin only)"""
        try:
            items = cart.get_all_cart_items()
            return [i.to_dict() for i in items]
        except Exception as e:
            api.abort(500, f"Error getting cart items: {str(e)}")


@api.route('/user/<string:user_id>')
class UserCart(Resource):
    def get(self, user_id):
        """Get all cart items for a user (includes artwork details + stock)"""
        try:
            items = cart.get_cart_items_by_user(user_id)
            return {
                'success': True,
                'data': items,
                'count': len(items)
            }
        except Exception as e:
            api.abort(500, f"Error getting user cart: {str(e)}")

    def delete(self, user_id):
        """Clear entire cart for a user"""
        try:
            if cart.clear_cart_for_user(user_id):
                return {"message": "Cart cleared successfully"}, 200
            return {"message": "Failed to clear cart"}, 400
        except Exception as e:
            api.abort(500, f"Error clearing cart: {str(e)}")


@api.route('/<int:cart_id>')
class CartItem(Resource):
    def get(self, cart_id):
        """Get a specific cart item by ID"""
        try:
            item = cart.get_cart_item_by_id(cart_id)
            if item:
                return item.to_dict()
            api.abort(404, "Cart item not found")
        except Exception as e:
            api.abort(500, f"Error getting cart item: {str(e)}")

    def put(self, cart_id):
        """Update quantity of a cart item (stock validated)"""
        data = request.json
        try:
            quantity = data.get('quantity')
            if not quantity or not isinstance(quantity, int) or quantity <= 0:
                api.abort(400, "Valid quantity is required")

            updated = cart.update_cart_item_quantity(cart_id, quantity)

            # Service may return (dict, status) for errors
            if isinstance(updated, tuple):
                payload, status = updated
                return payload, status

            if updated:
                return updated.to_dict()
            api.abort(404, "Cart item not found")
        except Exception as e:
            current_app.logger.error(f"Error updating cart item: {e}")
            api.abort(500, f"Error updating cart item: {str(e)}")

    def delete(self, cart_id):
        """Delete a cart item by ID"""
        try:
            if cart.delete_cart_item(cart_id):
                return {"message": "Item deleted successfully"}, 200
            return {"message": "Item not found"}, 404
        except Exception as e:
            api.abort(500, f"Error deleting cart item: {str(e)}")


@api.route('/total/<string:user_id>')
class CartTotal(Resource):
    def get(self, user_id):
        """Get total price of items in user's cart"""
        try:
            total = cart.get_cart_total(user_id)
            return {
                'user_id': user_id,
                'total': total
            }
        except Exception as e:
            api.abort(500, f"Error getting cart total: {str(e)}")


@api.route('/count/<string:user_id>')
class CartCount(Resource):
    def get(self, user_id):
        """Get total number of items in user's cart"""
        try:
            count = cart.get_cart_item_count(user_id)
            return {
                'user_id': user_id,
                'count': count
            }
        except Exception as e:
            api.abort(500, f"Error getting cart count: {str(e)}")


@api.route('/check/<string:user_id>/<string:artwork_id>')
class CartCheck(Resource):
    def get(self, user_id, artwork_id):
        """Check if an artwork is already in user's cart"""
        try:
            is_in_cart = cart.is_item_in_cart(user_id, artwork_id)
            return {
                'user_id': user_id,
                'artwork_id': artwork_id,
                'is_in_cart': is_in_cart
            }
        except Exception as e:
            api.abort(500, f"Error checking item in cart: {str(e)}")
