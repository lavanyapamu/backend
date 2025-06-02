from flask_restx import Namespace
 
class WishlistDTO:
    api = Namespace("wishlist", description="wishlist")