from app.main.models.payments import Payment
from init_db import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

def create_payment(order_id, amount, method, status):
    try:
        new_payment = Payment(
            order_id=order_id,
            amount=amount,
            method=method,
            status=status,
            payment_date=datetime.utcnow()
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment.to_dict(), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to create payment: {str(e)}"}, 500

def get_all_payments():
    try:
        payments = Payment.query.all()
        return [payment.to_dict() for payment in payments], 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch payments: {str(e)}"}, 500

def get_payment_by_id(payment_id):
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404
        return payment.to_dict(), 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch payment: {str(e)}"}, 500

def delete_payment(payment_id):
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            return {"error": "Payment not found"}, 404
        db.session.delete(payment)
        db.session.commit()
        return {"message": "Payment deleted successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to delete payment: {str(e)}"}, 500
