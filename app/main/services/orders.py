from datetime import datetime
from flask import current_app
from app.main.models.orders import Order
from app.main.utils.enums import Orderstatus
from init_db import db
from sqlalchemy.exc import SQLAlchemyError

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
    if not isinstance(new_status, str) or new_status not in Orderstatus.__members__:
        return {"error": f"Invalid status. Must be one of {list(Orderstatus.__members__.keys())}"}, 400

    try:
        order = Order.query.filter_by(order_id=order_id).first()
        if not order:
            return {"error": "Order not found"}, 404

        order.status = Orderstatus[new_status]
        order.updated_at = datetime.utcnow()
        db.session.commit()
        return {"message": "Order status updated"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to update order: {str(e)}"}, 500

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
