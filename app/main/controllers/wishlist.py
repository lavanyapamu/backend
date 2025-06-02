from flask import request
from flask_restx import Resource
from app.main.services.wishlist import (
    get_all_wishlist_items,
    get_wishlist_by_user,
    add_to_wishlist,
    remove_from_wishlist,
)
from app.main.dto.wishlist import UserDTO

api = UserDTO.api

@api.route("/")
class WishlistList(Resource):
    def get(self):
        """Get all wishlist items"""
        items = get_all_wishlist_items()
        return [item.__dict__ for item in items], 200

    def post(self):
        """Add an item to wishlist"""
        data = request.get_json()
        item = add_to_wishlist(data)
        return item.__dict__, 201

@api.route("/user/<uuid:user_id>")
class WishlistByUser(Resource):
    def get(self, user_id):
        """Get wishlist for a specific user"""
        items = get_wishlist_by_user(user_id)
        return [item.__dict__ for item in items], 200

@api.route("/<int:wishlist_id>")
class WishlistDelete(Resource):
    def delete(self, wishlist_id):
        """Remove an item from wishlist by ID"""
        success = remove_from_wishlist(wishlist_id)
        if success:
            return {"message": "Item removed from wishlist."}, 200
        return {"message": "Item not found."}, 404
