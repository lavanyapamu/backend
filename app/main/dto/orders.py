from flask_restx import Namespace, fields

class OrderDTO:
    api = Namespace("orders", description="Orders related operations")

    order = api.model("Order", {
        "order_id": fields.Integer(readonly=True),
        "user_id": fields.String(required=True, description="User UUID"),
        "total_price": fields.Float(required=True),
        "status": fields.String(description="Order status"),
        "created_at": fields.DateTime,
        "updated_at": fields.DateTime
    })

    order_status_update = api.model("OrderStatusUpdate", {
        "status": fields.String(required=True, description="New status")
    })
