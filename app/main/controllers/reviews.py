from flask_jwt_extended import jwt_required
from flask_restx import Resource
from flask import request
from app.main.dto.reviews import ReviewtDTO
from app.main.services.reviews import create_review, get_reviews_for_artwork

reviews_ns = ReviewtDTO.api


@reviews_ns.route("")
class ReviewList(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new review for an artwork (only if delivered order exists)
        """
        data = request.get_json()
        return create_review(data)


@reviews_ns.route("/artwork/<string:artwork_id>")
class ArtworkReviews(Resource):
    @jwt_required()
    def get(self, artwork_id):
        """
        Get all reviews for a specific artwork
        """
        return get_reviews_for_artwork(artwork_id)
