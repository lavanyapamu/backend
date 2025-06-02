from flask_restx import Namespace, fields
from app.main.utils.enums import PaymentStatus

class PaymentDTO:
    api = Namespace("payments", description="Payments operations")

    payment_request = api.model("PaymentRequest", {
        "order_id": fields.Integer(required=True, description="Order ID"),
        "user_id": fields.String(required=True, description="User UUID"),
        "amount": fields.Float(required=True, description="Payment amount"),
        "payment_method": fields.String(required=True, description="Payment method (e.g., 'credit_card', 'paypal')")
    })

    payment_response = api.model("PaymentResponse", {
        "payment_id": fields.Integer(description="Payment ID"),
        "order_id": fields.Integer(description="Order ID"),
        "user_id": fields.String(description="User UUID"),
        "amount": fields.Float(description="Amount paid"),
        "payment_method": fields.String(description="Payment method"),
        "status": fields.String(enum=[status.value for status in PaymentStatus], description="Payment status"),
        "created_at": fields.DateTime(description="Payment timestamp")
    })
