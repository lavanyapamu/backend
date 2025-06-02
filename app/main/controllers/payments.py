from flask_restx import Resource
from flask import request
from app.main.dto.payments import PaymentDTO
from app.main.services.payments import (
    create_payment, get_all_payments, get_payment_by_id, delete_payment
)

api = PaymentDTO.api
payment_request = PaymentDTO.payment_request
payment_response = PaymentDTO.payment_response

@api.route('/')
class PaymentList(Resource):
    @api.marshal_list_with(payment_response)
    def get(self):
        """Get all payments"""
        return get_all_payments()

    @api.expect(payment_request, validate=True)
    @api.marshal_with(payment_response, code=201)
    def post(self):
        """Create a new payment"""
        data = request.json
        return create_payment(data)

@api.route('/<int:payment_id>')
@api.param('payment_id', 'The Payment ID')
class PaymentResource(Resource):
    @api.marshal_with(payment_response)
    def get(self, payment_id):
        """Get payment by ID"""
        return get_payment_by_id(payment_id)

    def delete(self, payment_id):
        """Delete a payment"""
        return delete_payment(payment_id)
