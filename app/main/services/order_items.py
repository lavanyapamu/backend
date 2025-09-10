from flask_jwt_extended import get_jwt_identity
from app.main.models.artworks import Artwork
from app.main.models.order_items import OrderItem
from app.main.models.user import User
from app.main.services.orders import update_overall_order_status
from app.main.utils.enums import Orderstatus
from init_db import db
from sqlalchemy.exc import SQLAlchemyError

def create_order_item(order_id, artwork_id, quantity):
    try:
        if quantity <= 0:
            return {"error": "Quantity must be positive."}, 400

        artwork = Artwork.query.get(artwork_id)
        if not artwork:
            return {"error": "Artwork not found."}, 404

        new_item = OrderItem(
            order_id=order_id,
            artwork_id=artwork_id,
            quantity=quantity,
            price=artwork.price  # snapshot the artwork price at time of order
        )
        db.session.add(new_item)
        artwork.quantity -= quantity
        db.session.commit()
        return {"message": "Order item created", 
                "order_item_id": str(new_item.order_item_id), 
                "remaining_stock": artwork.quantity}, 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to create order item: {str(e)}"}, 500


def get_order_items_by_order(order_id):
    try:
        items = OrderItem.query.filter_by(order_id=order_id).all()
        return [item.to_dict() for item in items], 200
    except SQLAlchemyError as e:
        return {"error": f"Failed to fetch order items: {str(e)}"}, 500

def delete_order_item(order_item_id):
    try:
        item = OrderItem.query.filter_by(order_item_id=order_item_id).first()
        if not item:
            return {"error": "Order item not found"}, 404
        db.session.delete(item)
        db.session.commit()
        return {"message": "Order item deleted"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to delete order item: {str(e)}"}, 500

def update_order_item_status(order_item_id, new_status):
    """
    Update a single order item's status.
    Only artist of the artwork or admin can update.
    Adjust earnings and sales count for delivered/returned/refunded.
    Automatically recalculates overall order status.
    """
    identity = get_jwt_identity()
    user_id = identity["user_id"]
    user = User.query.get(user_id)

    if not isinstance(new_status, str):
        return {"error": "Invalid status type"}, 400

    new_status = new_status.lower().strip()
    allowed_statuses = [name.lower() for name in Orderstatus.__members__]
    if new_status not in allowed_statuses:
        return {"error": f"Invalid status. Must be one of {allowed_statuses}"}, 400

    item = OrderItem.query.get(order_item_id)
    if not item:
        return {"error": "Order item not found"}, 404

    role = user.role.role_name.lower()
    if role == "artist" and user.user_id != item.artwork.artist_id:
        return {"error": "Unauthorized to update this item"}, 403

    try:
        old_status = item.status.value if isinstance(item.status, Orderstatus) else str(item.status).lower()
        item.status = Orderstatus[new_status]

        # Handle delivered → update earnings & sales count
        if old_status != "delivered" and new_status == "delivered":
            artist = item.artwork.artist
            total_price = item.price * item.quantity
            artist.earnings = (artist.earnings or 0) + total_price
            item.artwork.sales_count = (item.artwork.sales_count or 0) + item.quantity

        # Handle returned/refunded
        elif old_status == "delivered" and new_status in ["returned", "refunded"]:
            artist = item.artwork.artist
            total_price = item.price * item.quantity
            artist.earnings = max(0, (artist.earnings or 0) - total_price)
            item.artwork.sales_count = max(0, (item.artwork.sales_count or 0) - item.quantity)

        # Recalculate overall order status
        update_overall_order_status(item.order_id)

        db.session.commit()
        return {"message": "Order item status updated successfully"}, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": f"Failed to update order item: {str(e)}"}, 500