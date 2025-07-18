# services/cart_service.py
from flask import current_app
from app.main.models.cart import Cart
from app.main.models.artworks import Artwork
from init_db import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

def get_all_cart_items():
    """Get all cart items"""
    try:
        return Cart.query.all()
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error getting all cart items: {e}")
        raise e

def get_cart_items_by_user(user_id):
    """Get all cart items for a specific user"""
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        result = []
        
        for item in cart_items:
            # Get artwork details
            artwork = Artwork.query.filter_by(artwork_id=item.artwork_id, is_deleted=False).first()
            if artwork:
                item_dict = {
                    'cart_id': item.cart_id,
                    'user_id': str(item.user_id),
                    'artwork_id': str(item.artwork_id),
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'added_at': item.added_at.isoformat() if item.added_at else None,
                    'artwork': {
                        'title': artwork.title,
                        'description': artwork.description,
                        'category': artwork.category_name.name if artwork.category_name else None,
                        'style': artwork.style.name if artwork.style else None,
                        'image': artwork.art_image,
                        'artist_id': str(artwork.artist_id)
                    }
                }
                result.append(item_dict)
        
        return result
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error getting cart items for user {user_id}: {e}")
        raise e

def add_to_cart(data):
    """Add an item to cart"""
    try:
        # Check if item already exists in cart
        existing_item = Cart.query.filter_by(
            user_id=data['user_id'],
            artwork_id=data['artwork_id']
        ).first()
        
        if existing_item:
            # Update quantity if item already exists
            existing_item.quantity += data.get('quantity', 1)
            existing_item.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return existing_item
        
        # Create new cart item
        new_item = Cart(
            user_id=data['user_id'],
            artwork_id=data['artwork_id'],
            quantity=data.get('quantity', 1),
            price=data['price'],
            added_at=datetime.now(timezone.utc)
        )
        
        db.session.add(new_item)
        db.session.commit()
        return new_item
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error adding item to cart: {e}")
        raise e

def update_cart_item_quantity(cart_id, quantity):
    """Update quantity of a cart item"""
    try:
        cart_item = Cart.query.get(cart_id)
        if cart_item:
            cart_item.quantity = quantity
            cart_item.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return cart_item
        return None
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating cart item {cart_id}: {e}")
        raise e

def delete_cart_item(cart_id):
    """Delete a cart item by ID"""
    try:
        cart_item = Cart.query.get(cart_id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return True
        return False
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting cart item {cart_id}: {e}")
        raise e

def clear_cart_for_user(user_id):
    """Clear entire cart for a user"""
    try:
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True
        
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Error clearing cart for user {user_id}: {e}")
        raise e

def get_cart_total(user_id):
    """Get total price of items in user's cart"""
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        total = sum(item.price * item.quantity for item in cart_items)
        return float(total)
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error calculating cart total for user {user_id}: {e}")
        raise e

def get_cart_item_count(user_id):
    """Get total number of items in user's cart"""
    try:
        return Cart.query.filter_by(user_id=user_id).count()
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error getting cart count for user {user_id}: {e}")
        raise e

def get_cart_item_by_id(cart_id):
    """Get a specific cart item by ID"""
    try:
        return Cart.query.get(cart_id)
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error getting cart item {cart_id}: {e}")
        raise e

def is_item_in_cart(user_id, artwork_id):
    """Check if an artwork is already in user's cart"""
    try:
        return Cart.query.filter_by(
            user_id=user_id,
            artwork_id=artwork_id
        ).first() is not None
        
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error checking if item in cart: {e}")
        raise e