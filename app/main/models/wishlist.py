from init_db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    wishlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    artwork_id = db.Column(UUID(as_uuid=True), db.ForeignKey('artworks.artwork_id', ondelete='CASCADE'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="wishlist")
    artwork = db.relationship("Artwork", lazy=True)

    def __repr__(self):
        return f"<Wishlist {self.wishlist_id} - User {self.user_id} - Artwork {self.artwork_id}>"


    def to_dict(self):
        return {
            "wishlist_id": self.wishlist_id,
            "user_id": str(self.user_id),
            "artwork_id": str(self.artwork_id),
            "price": self.price,
            "added_at": self.added_at.isoformat(),
            "artwork": self.artwork.to_dict() if self.artwork else None
        }
