# dto/cart_dto.py

from flask_restx import Namespace

class CartDTO:
    api = Namespace("cart", description="Cart operations")

    
