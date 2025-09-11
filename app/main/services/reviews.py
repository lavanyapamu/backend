from app.main.models.reviews import Review
from app.main.models.orders import Order
from app.main.utils.enums import Orderstatus
from init_db import db
from sqlalchemy.exc import SQLAlchemyError


from app.main.models.order_items import OrderItem

def create_review(data):
    try:
        user_id = data.get("user_id")
        artwork_id = data.get("artwork_id")
        rating = data.get("rating")
        review_text = data.get("review_text", "No review provided")

        if not user_id or not artwork_id or not rating:
            return {"message": "user_id, artwork_id and rating are required"}, 400

        # ✅ Ensure order exists and delivered
        order = (
            Order.query
            .filter(
                Order.user_id == user_id,
                Order.status == Orderstatus.delivered
            )
            .filter(Order.order_items.any(artwork_id=artwork_id))
            .first()
        )

        if not order:
            return {"message": "User can only review artworks they purchased and received"}, 403

        # ✅ Prevent duplicate review
        existing = Review.query.filter_by(user_id=user_id, artwork_id=artwork_id).first()
        if existing:
            return {"message": "You have already reviewed this artwork"}, 409

        # ✅ Save review
        review = Review(
            user_id=user_id,
            artwork_id=artwork_id,
            rating=rating,
            review_text=review_text,
        )
        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"[SQLAlchemyError] {str(e)}")  # 👈 print for logs
        return {"message": str(e)}, 500

    except Exception as e:
        db.session.rollback()
        print(f"[UnexpectedError] {str(e)}")  # 👈 catch all other errors
        return {"message": str(e)}, 500




def get_reviews_for_artwork(artwork_id):
    try:
        reviews = Review.query.filter_by(artwork_id=artwork_id).all()
        return [r.to_dict() for r in reviews], 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500
