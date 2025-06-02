from app.main.models.order_items import OrderItem
from app.main.models.orders import Order
from manage import db

def create_order_item(order_id, artwork_id, quantity, price):
    try:
        if quantity <= 0 or price < 0:
            return {"error": "Quantity and price must be positive."}, 400

        new_item = OrderItem(
            order_id=order_id,
            artwork_id=artwork_id,
            quantity=quantity,
            price=price
        )
        db.session.add(new_item)
        db.session.commit()
        return {"message": "Order item created", "order_item_id": new_item.order_item_id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to create order item: {str(e)}"}, 500


def get_order_items_by_order(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    return [item.to_dict() for item in items], 200


def delete_order_item(order_item_id):
    item = OrderItem.query.filter_by(order_item_id=order_item_id).first()
    if not item:
        return {"error": "Order item not found"}, 404

    try:
        db.session.delete(item)
        db.session.commit()
        return {"message": "Order item deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete order item: {str(e)}"}, 500
