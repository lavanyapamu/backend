
# from flask import Blueprint
# from flask_restx import Api

# from app.main.controllers import artworks
# blueprint = Blueprint("api", __name__)
# api = Api(blueprint, title="ArtFlare API", version="1.0", description="ArtFlare Backend API")

# # Controller imports
# from app.main.dto.user import UserDTO
# users_ns = UserDTO.api

# from app.main.dto.artworks import ArtworkDTO
# artworks_ns =  ArtworkDTO.api

# from app.main.dto.orders  import OrderDTO
# orders_ns =  OrderDTO.api

# from app.main.dto.order_items import OrderItemDTO
# order_items_ns =  OrderItemDTO.api

# from app.main.dto.cart import CartDTO
# cart_ns =  CartDTO.api

# from app.main.dto.wishlist import WishlistDTO
# wishlist_ns =  WishlistDTO.api

# from app.main.dto.reviews import ReviewDTO
# reviews_ns =  ReviewDTO.api

# from app.main.dto.payments import PaymentDTO
# payments_ns =  PaymentDTO.api

# # Namespace registrations
# api.add_namespace(users_ns)
# api.add_namespace(artworks_ns,  path="/artworks")
# api.add_namespace(orders_ns)
# api.add_namespace(order_items_ns)
# api.add_namespace(cart_ns)
# api.add_namespace(wishlist_ns)
# api.add_namespace(reviews_ns)
# api.add_namespace(payments_ns)


