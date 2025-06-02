from init_db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.main.utils.enums import PaymentStatus

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # Validate in app layer or enums if defined
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="payments")
    order = db.relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.payment_id} - Order {self.order_id} - User {self.user_id} - Status {self.status.value}>"



def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "user_id": str(self.user_id),
            "amount": self.amount,
            "payment_method": self.payment_method,
            "status": self.status.value,
            "created_at": self.created_at.isoformat()  # Use isoformat for JSON serialization
        }
