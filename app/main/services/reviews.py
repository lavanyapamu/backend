from app.main.models.reviews import Review
from init_db import db
from sqlalchemy.exc import SQLAlchemyError

def create_review(data):
    try:
        review = Review(
            user_id=data["user_id"],
            artwork_id=data["artwork_id"],
            rating=data["rating"],
            review_text=data.get("review_text", "No review provided")
        )
        db.session.add(review)
        db.session.commit()
        return review.to_dict(), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500

def get_all_reviews():
    reviews = Review.query.all()
    return [r.to_dict() for r in reviews], 200

def get_review_by_id(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"message": "Review not found"}, 404
    return review.to_dict(), 200

def update_review(review_id, data):
    review = Review.query.get(review_id)
    if not review:
        return {"message": "Review not found"}, 404
    try:
        review.rating = data.get("rating", review.rating)
        review.review_text = data.get("review_text", review.review_text)
        db.session.commit()
        return review.to_dict(), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500

def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return {"message": "Review not found"}, 404
    try:
        db.session.delete(review)
        db.session.commit()
        return {"message": "Review deleted successfully"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": str(e)}, 500
