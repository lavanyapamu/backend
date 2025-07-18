from init_db import db
from app.main.utils.enums import CategoryName,StyleType
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Artwork(db.Model):
    __tablename__ = 'artworks'

    artwork_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_name = db.Column(db.Enum(CategoryName),  nullable=False)
    style = db.Column(db.Enum(StyleType, nullable=False))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    art_image = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sales_count = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    

    
    artist = db.relationship('User', back_populates='artworks')
    reviews = db.relationship("Review", back_populates="artwork", lazy=True)

    def __repr__(self):
        return f"<Artwork {self.title} by {self.artist_id}>"

    def to_dict(self):
        return {
            "artwork_id": str(self.artwork_id),
            "artist_id": str(self.artist_id),
            "title": self.title,
            "description": self.description,
            "category_name": self.category_name.value,
            "style": self.style.value,
            "price": self.price,
            "quantity": self.quantity,
            "sales_count": self.sales_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "image": self.art_image,
            "is_deleted": self.is_deleted
        }
