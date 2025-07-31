from init_db import db
from datetime import datetime
from app.main.utils.enums import Orderstatus
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(Orderstatus), nullable=False, default=Orderstatus.pending)
    
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy=True)
    payment = db.relationship("Payment", back_populates="order", uselist=False)

    def __repr__(self):
        return f"<Order {self.order_id} - User {self.user_id} - Status {self.status.value}>"

    def to_dict(self):
        return {
            "order_id": str(self.order_id),
            "user_name":self.user.full_name,
            "user_id": str(self.user_id),
            "total_price": self.total_price,
            "status": self.status.value,
            "items": [item.to_dict() for item in self.order_items],
            "payment": self.payment.to_dict() if self.payment else None,
            "created_at": self.order_date.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
