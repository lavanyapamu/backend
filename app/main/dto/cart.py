# dto/cart_dto.py

from flask_restx import Namespace, fields

class CartDTO:
    api = Namespace("cart", description="Cart operations")

    cart_request = api.model("CartRequest", {
        "user_id": fields.String(required=True, description="User UUID"),
        "artwork_id": fields.String(required=True, description="Artwork UUID"),
        "quantity": fields.Integer(required=True, description="Quantity"),
        "price": fields.Float(required=True, description="Price of the item"),
    })

    cart_response = api.model("CartResponse", {
        "cart_id": fields.Integer(description="Cart ID"),
        "user_id": fields.String(description="User UUID"),
        "artwork_id": fields.String(description="Artwork UUID"),
        "quantity": fields.Integer(description="Quantity"),
        "price": fields.Float(description="Price"),
        "added_at": fields.DateTime(description="Date item was added to cart")
    })
