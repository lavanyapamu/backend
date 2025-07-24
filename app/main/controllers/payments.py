from flask import request
from flask_restx import Resource
from app.main.dto.payments import PaymentDTO
from app.main.services.payments import (
    create_payment,
    get_all_payments,
    get_payment_by_id,
    delete_payment
)

api = PaymentDTO.api

@api.route('/')
class PaymentList(Resource):
    def get(self):
        return get_all_payments()

    def post(self):
        data = request.get_json()
        return create_payment(
            order_id=data['order_id'],
            amount=data['amount'],
            method=data['method'],
            status=data['status']
        )

@api.route('/<uuid:payment_id>')
class PaymentResource(Resource):
    def get(self, payment_id):
        return get_payment_by_id(payment_id)

    def delete(self, payment_id):
        return delete_payment(payment_id)
