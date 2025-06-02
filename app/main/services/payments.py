from app.main.models.payments import Payment
from init_db import db
from app.main.utils.enums import PaymentStatus
from sqlalchemy.exc import SQLAlchemyError

def create_payment(data):
    try:
        payment = Payment(
            order_id=data["order_id"],
            user_id=data["user_id"],
            amount=data["amount"],
            payment_method=data["payment_method"],
            status=PaymentStatus.success  # Modify for real integration/payment gateway status
        )
        db.session.add(payment)
        db.session.commit()
        return payment.to_dict(), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500

def get_all_payments():
    payments = Payment.query.all()
    return [payment.to_dict() for payment in payments], 200

def get_payment_by_id(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return {"message": "Payment not found"}, 404
    return payment.to_dict(), 200

def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return {"message": "Payment not found"}, 404
    db.session.delete(payment)
    db.session.commit()
    return {"message": "Payment deleted successfully"}, 200
