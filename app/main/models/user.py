from init_db import db
from app.main.utils.enums import Userstatus, Orderstatus, PaymentStatus
from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID,ENUM
import uuid

class User(db.Model):
    __tablename__ = 'users'
    user_id=db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    role_id = db.Column(db.SmallInteger, db.ForeignKey('roles.role_id'), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True) 
    earnings = db.Column(db.Float, default=0.00)
    wallet= db.Column(db.Float, nullable=False, default=0.00)
    status=db.Column(db.Enum(Userstatus), nullable=False, default=Userstatus.pending)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)
    password = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    role = db.relationship('Role', back_populates='users')
    artworks = db.relationship("Artwork", back_populates="artist", lazy=True)
    orders = db.relationship("Order", back_populates="user", lazy=True)
    orders = db.relationship("Order", back_populates="user", lazy=True)
    payment = db.relationship("Payment", back_populates="user", lazy=True)
    reviews = db.relationship("Review", back_populates="user", lazy=True)
    cart= db.relationship("Cart", back_populates="user", lazy=True)
    wishlist= db.relationship("Wishlist", back_populates="user", lazy=True)

    def __repr__(self):
     return f"<User {self.user_id} - {self.email} - {self.status.value}>"

    def to_dict(self):
        return {
            "user_id": str(self.user_id),
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role_id": self.role_id,
            "earnings": self.earnings,
            "status": self.status.value,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "profile_image": self.profile_image

            # Excluding profile_image and password for privacy and performance
        }