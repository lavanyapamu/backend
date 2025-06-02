from app.main.models.wishlist import Wishlist
from init_db import db
from sqlalchemy.exc import SQLAlchemyError

def get_all_wishlist_items():
    return Wishlist.query.all()

def get_wishlist_by_user(user_id):
    return Wishlist.query.filter_by(user_id=user_id).all()

def add_to_wishlist(data):
    try:
        new_item = Wishlist(
            user_id=data['user_id'],
            artwork_id=data['artwork_id'],
            price=data['price']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e

def remove_from_wishlist(wishlist_id):
    item = Wishlist.query.get(wishlist_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False
