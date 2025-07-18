from app.main.models.wishlist import Wishlist
from init_db import db
from sqlalchemy.exc import SQLAlchemyError
import logging

# Set up logging
logger = logging.getLogger(__name__)

def get_all_wishlist_items():
    """Get all wishlist items"""
    try:
        return Wishlist.query.all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching all wishlist items: {str(e)}")
        raise e

def get_wishlist_by_user(user_id):
    """Get wishlist items for a specific user"""
    try:
        return Wishlist.query.filter_by(user_id=user_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Error fetching wishlist for user {user_id}: {str(e)}")
        raise e

def add_to_wishlist(data):
    """Add item to wishlist"""
    try:
        # Check if item already exists in wishlist
        existing_item = Wishlist.query.filter_by(
            user_id=data['user_id'],
            artwork_id=data['artwork_id']
        ).first()
        
        if existing_item:
            return {"error": "Item already exists in wishlist"}, 400
        
        new_item = Wishlist(
            user_id=data['user_id'],
            artwork_id=data['artwork_id'],
            price=data['price']
        )
        db.session.add(new_item)
        db.session.commit()
        logger.info(f"Item added to wishlist for user {data['user_id']}")
        return new_item
    except SQLAlchemyError as e:
        logger.error(f"Error adding to wishlist: {str(e)}")
        db.session.rollback()
        raise e
    except Exception as e:
        logger.error(f"Unexpected error adding to wishlist: {str(e)}")
        db.session.rollback()
        raise e

def remove_from_wishlist(wishlist_id):
    """Remove item from wishlist"""
    try:
        item = Wishlist.query.get(wishlist_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            logger.info(f"Item {wishlist_id} removed from wishlist")
            return True
        return False
    except SQLAlchemyError as e:
        logger.error(f"Error removing from wishlist: {str(e)}")
        db.session.rollback()
        raise e

def check_item_in_wishlist(user_id, artwork_id):
    """Check if item exists in user's wishlist"""
    try:
        return Wishlist.query.filter_by(
            user_id=user_id,
            artwork_id=artwork_id
        ).first() is not None
    except SQLAlchemyError as e:
        logger.error(f"Error checking item in wishlist: {str(e)}")
        raise e