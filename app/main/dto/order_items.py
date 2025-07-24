from flask_restx import Namespace
 
class OrderItemDTO:
    api = Namespace("order-items", description="Order Item operations")