from init_db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    artwork_id = db.Column(UUID(as_uuid=True), db.ForeignKey('artworks.artwork_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="cart")
    artwork = db.relationship("Artwork", lazy=True)

    def __repr__(self):
        return f"<Cart {self.cart_id} - User {self.user_id} - Artwork {self.artwork_id} - Qty {self.quantity}>"

def to_dict(self):
        return {
            "cart_id": self.cart_id,
            "user_id": str(self.user_id),
            "artwork_id": str(self.artwork_id),
            "quantity": self.quantity,
            "price": self.price,
            "added_at": self.added_at.isoformat()
        }
