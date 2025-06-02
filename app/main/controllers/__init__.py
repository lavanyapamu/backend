
from flask import Blueprint
from flask_restx import Api
from app.main.controllers.artworks import artwork_ns
from app.main.controllers.user import user_ns
blueprint = Blueprint("api", __name__)
api = Api(blueprint, title="ArtFlare API", version="1.0", description="ArtFlare Backend API")

api.add_namespace(artwork_ns,  path="/artworks")
# api.add_namespace(orders_ns)
# api.add_namespace(order_items_ns)
# api.add_namespace(cart_ns)
# api.add_namespace(wishlist_ns)
# api.add_namespace(reviews_ns)
# api.add_namespace(payments_ns)
api.add_namespace(user_ns, path="/users")


