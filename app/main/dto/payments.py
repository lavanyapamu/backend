from flask_restx import Namespace

class PaymentDTO:
    api = Namespace("payments", description="Payment operations")