from init_db import db
from sqlalchemy.dialects.postgresql import UUID

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    artwork_id = db.Column(UUID(as_uuid=True), db.ForeignKey('artworks.artwork_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    artwork = db.relationship("Artwork", lazy=True)

    def __repr__(self):
        return f"<OrderItem {self.order_item_id} - Order {self.order_id} - Artwork {self.artwork_id} - Quantity {self.quantity}>"



def to_dict(self):
    return {
        "order_item_id": self.order_item_id,
        "order_id": self.order_id,
        "artwork_id": str(self.artwork_id),
        "quantity": self.quantity,
        "price": self.price
    }
