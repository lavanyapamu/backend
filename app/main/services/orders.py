from datetime import datetime, timezone
from app.main.models.orders import Order, OrderStatusEnum
from app.main.models.user import User
from manage import db

def create_order(user_id, total_price):
    try:
        if total_price < 0:
            return {"error": "Total price cannot be negative."}, 400

        new_order = Order(
            user_id=user_id,
            total_price=total_price,
            status=OrderStatusEnum.PENDING,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        db.session.add(new_order)
        db.session.commit()

        return {"message": "Order created successfully", "order_id": new_order.order_id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to create order: {str(e)}"}, 500


def get_orders_by_user(user_id):
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return [order.to_dict() for order in orders], 200


def get_order_by_id(order_id, user_id=None):
    query = Order.query.filter_by(order_id=order_id)
    if user_id:
        query = query.filter_by(user_id=user_id)

    order = query.first()
    if not order:
        return {"error": "Order not found"}, 404
    return order.to_dict(), 200


def update_order_status(order_id, new_status):
    if new_status not in OrderStatusEnum.ALL:
        return {"error": "Invalid status"}, 400

    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return {"error": "Order not found"}, 404

    try:
        order.status = new_status
        order.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return {"message": "Order status updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update order: {str(e)}"}, 500


def delete_order(order_id, user_id=None):
    query = Order.query.filter_by(order_id=order_id)
    if user_id:
        query = query.filter_by(user_id=user_id)

    order = query.first()
    if not order:
        return {"error": "Order not found"}, 404

    try:
        db.session.delete(order)
        db.session.commit()
        return {"message": "Order deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete order: {str(e)}"}, 500
