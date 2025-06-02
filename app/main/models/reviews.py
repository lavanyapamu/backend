from init_db import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    artwork_id = db.Column(UUID(as_uuid=True), db.ForeignKey('artworks.artwork_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    review_text = db.Column(db.Text, nullable=True, default="No review provided")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="reviews")
    artwork = db.relationship("Artwork", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.review_id} - User {self.user_id} - Artwork {self.artwork_id} - Rating {self.rating}>"
    
def to_dict(self):
        return {
            "review_id": self.review_id,
            "user_id": str(self.user_id),
            "artwork_id": str(self.artwork_id),
            "rating": self.rating,
            "review_text": self.review_text,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }