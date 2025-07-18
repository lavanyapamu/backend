from flask import request, jsonify
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.main.services.wishlist import (
    get_all_wishlist_items,
    get_wishlist_by_user,
    add_to_wishlist,
    remove_from_wishlist,
    check_item_in_wishlist
)
from app.main.dto.wishlist import WishlistDTO

api = WishlistDTO.api
logger = logging.getLogger(__name__)

def serialize_wishlist_item(item):
    return item.to_dict()

@api.route("/")
class WishlistList(Resource):
    def get(self):
        try:
            items = get_all_wishlist_items()
            return [item.to_dict() for item in items], 200
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"error": "No data provided"}, 400

            required_fields = ['user_id', 'artwork_id', 'price']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

            if check_item_in_wishlist(data['user_id'], data['artwork_id']):
                return {"error": "Item already exists in wishlist"}, 400

            item = add_to_wishlist(data)
            logger.info(f"Item added: {item}")
            return serialize_wishlist_item(item), 201

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

@api.route("/user/<uuid:user_id>")
class WishlistByUser(Resource):
    def get(self, user_id):
        """Get wishlist for a specific user"""
        try:
            items = get_wishlist_by_user(user_id)
            return [serialize_wishlist_item(item) for item in items], 200
        except SQLAlchemyError as e:
            logger.error(f"Database error in get user wishlist: {str(e)}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logger.error(f"Unexpected error in get user wishlist: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

@api.route("/<int:wishlist_id>")
class WishlistDelete(Resource):
    def delete(self, wishlist_id):
        """Remove an item from wishlist by ID"""
        try:
            success = remove_from_wishlist(wishlist_id)
            if success:
                return {"message": "Item removed from wishlist."}, 200
            return {"message": "Item not found."}, 404
        except SQLAlchemyError as e:
            logger.error(f"Database error in delete wishlist item: {str(e)}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logger.error(f"Unexpected error in delete wishlist item: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500

@api.route("/check/<uuid:user_id>/<uuid:artwork_id>")
class WishlistCheck(Resource):
    def get(self, user_id, artwork_id):
        """Check if item exists in user's wishlist"""
        try:
            exists = check_item_in_wishlist(user_id, artwork_id)
            return {"exists": exists}, 200
        except SQLAlchemyError as e:
            logger.error(f"Database error in check wishlist: {str(e)}")
            return {"error": "Database error occurred"}, 500
        except Exception as e:
            logger.error(f"Unexpected error in check wishlist: {str(e)}")
            return {"error": "An unexpected error occurred"}, 500