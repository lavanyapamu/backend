# models/payments.py
from init_db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship("Order", back_populates="payment")

    def to_dict(self):
        return {
            "id": str(self.id),
            "order_id": str(self.order_id),
            "amount": self.amount,
            "method": self.method,
            "status": self.status,
            "payment_date": self.payment_date.isoformat()
        }
