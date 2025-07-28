from init_db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'), nullable=False)
    artwork_id = db.Column(UUID(as_uuid=True), db.ForeignKey('artworks.artwork_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", back_populates="order_items")
    artwork = db.relationship("Artwork", back_populates="order_items")

    def to_dict(self):
        return {
            "order_item_id": str(self.order_item_id),
            "order_id": str(self.order_id),
            "artwork_id": str(self.artwork_id),
            "quantity": self.quantity,
            "price": self.price,
            "artwork": self.artwork.to_dict() if self.artwork else None
        }
