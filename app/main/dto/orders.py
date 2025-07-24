from flask_restx import Namespace

class OrderDTO:
    api = Namespace("orders", description="Order operations")
