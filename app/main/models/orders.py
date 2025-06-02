from init_db import db
from datetime import datetime
from app.main.utils.enums import Orderstatus
from sqlalchemy.dialects.postgresql import UUID

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(Orderstatus), nullable=False, default=Orderstatus.pending)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

 
    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy=True)
    payments = db.relationship("Payment", back_populates="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.order_id} - User {self.user_id} - Status {self.status.value}>"


    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
