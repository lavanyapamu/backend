from init_db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app.main.utils.enums import PaymentStatus
import uuid

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'), nullable=False, unique=True)

    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)

    city = db.Column(db.String(256), nullable=False)
    state = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(256), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    
    upi_id = db.Column(db.String(100), nullable=True)
    

    shipping_fee = db.Column(db.Numeric(10, 2), nullable=True, default=0.00)
    subtotal = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    wallet = db.Column(db.Float, nullable=True, default=0.00)

    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order = db.relationship("Order", back_populates="payment")
    user = db.relationship("User", back_populates="payment")

    def to_dict(self):
        return {
            "payment_id": str(self.payment_id),
            "user_id": str(self.user_id),
            "order_id": str(self.order_id),
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "pincode": self.pincode,
            "payment_method": self.payment_method,
            "wallet": float(self.wallet or 0.0),
            "upi_id": self.upi_id,
            "shipping_fee": float(self.shipping_fee or 0.00),
            "subtotal": self.subtotal,
            "total": self.total,
            "status": self.status.value,
            "payment_date": self.payment_date.isoformat()
        }
