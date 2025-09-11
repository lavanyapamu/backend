from datetime import datetime
from flask import current_app, jsonify
from app.main.models.artworks import Artwork
from app.main.models.order_items import OrderItem
from app.main.models.orders import Order
from app.main.models.user import User
from app.main.utils.enums import Orderstatus
from init_db import db
from flask_jwt_extended import get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

def create_order(user_id, total_price):
    try:
        if total_price < 0:
            return {"error": "Total price cannot be negative."}, 400

        new_order = Order(
            user_id=user_id,
            total_price=total_price,
            status=Orderstatus.pending
        )

        db.session.add(new_order)
        db.session.commit()
        return {"message": "Order created", "order_id": str(new_order.order_id)}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Create Order Error: {str(e)}")
        return {"error": f"Failed to create order: {str(e)}"}, 500
    
def get_all_orders():
    """Get all orders for artist dashboard"""
    try:
        orders = Order.query.order_by(Order.order_date.desc()).all()
        return [order.to_dict() for order in orders], 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch all orders: {str(e)}"}, 500  
    
def get_orders_by_user(user_id):
    try:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()
        return [order.to_dict() for order in orders], 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch orders: {str(e)}"}, 500
    
def get_orders_for_artist(artist_id, limit=None):
    try:
        query = (
            Order.query
            .join(OrderItem, Order.order_id == OrderItem.order_id)
            .join(Artwork, OrderItem.artwork_id == Artwork.artwork_id)
            .filter(Artwork.artist_id == artist_id)
            .options(
                joinedload(Order.order_items).joinedload(OrderItem.artwork),
                joinedload(Order.user)
            )
            .order_by(Order.order_date.desc())
        )

        if limit:
            query = query.limit(limit)

        orders = query.all()

        if not orders:
            return {
                "message": "No orders found for this artist",
                "orders": [],
                "count": 0,
                "earnings": 0
            }, 200

        orders_list = []
        for order in orders:
            order_dict = order.to_dict(artist_id=artist_id)
            if order_dict["items"]:
                orders_list.append(order_dict)
        artist = User.query.get(artist_id)
        return {
            "message": "Artist orders fetched successfully",
            "orders": orders_list,
            "count": len(orders_list),
             "count": len(orders_list),
            "earnings": artist.earnings if artist and artist.earnings else 0
        }, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Get Artist Orders Error: {str(e)}")
        return {
            "error": f"Failed to fetch artist orders: {str(e)}"
        }, 500



def get_order_by_id(order_id, user_id=None):
    try:
        query = Order.query.filter_by(order_id=order_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        order = query.first()
        if not order:
            return {"error": "Order not found"}, 404
        return order.to_dict(), 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch order: {str(e)}"}, 500
    
def update_order_status(order_id, new_status):
    """
    Update overall order status (admin-only use).
    """
    try:
        order = Order.query.get(order_id)
        if not order:
            return {"error": "Order not found"}, 404

        if not isinstance(new_status, str):
            return {"error": "Invalid status type"}, 400

        new_status = new_status.lower().strip()
        allowed_statuses = [name.lower() for name in Orderstatus.__members__]
        if new_status not in allowed_statuses:
            return {"error": f"Invalid status. Must be one of {allowed_statuses}"}, 400

        order.status = Orderstatus[new_status]
        order.updated_at = datetime.utcnow()
        db.session.commit()
        return {"message": "Order status updated successfully"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to update order: {str(e)}"}, 500


def update_overall_order_status(order_id):
    """
    Recalculate and update overall order status based on item statuses.
    Called from OrderItem service when an item status changes.
    """
    order = Order.query.get(order_id)
    if not order:
        return {"error": "Order not found"}, 404

    # item_statuses = [item.status for item in order.order_items]
    item_statuses = [
        item.status.value if isinstance(item.status, Orderstatus) else str(item.status).lower()
        for item in order.order_items
    ]


     # Determine overall status
    if all(s == 'cancelled' for s in item_statuses):
        new_status = 'cancelled'
    elif all(s == 'delivered' for s in item_statuses):
        new_status = 'delivered'
    elif all(s == 'shipped' for s in item_statuses):
        new_status = 'shipped'
    elif all(s == 'confirmed' for s in item_statuses):
        new_status = 'confirmed'
    else:
        new_status = 'pending'  # mixed statuses

    # Save string to DB
    order.status = new_status
    order.updated_at = datetime.utcnow()
    db.session.commit()


def delete_order(order_id, user_id=None):
    try:
        query = Order.query.filter_by(order_id=order_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        order = query.first()
        if not order:
            return {"error": "Order not found"}, 404

        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to delete order: {str(e)}"}, 500
