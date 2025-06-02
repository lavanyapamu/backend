from flask_restx import Namespace
 
class OrderItemDTO:
    api = Namespace("order_items", description="order_items")