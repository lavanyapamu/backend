from flask_restx import Resource
from flask import request
from app.main.dto.reviews import ReviewDTO
from app.main.services.reviews import (
    create_review, get_all_reviews, get_review_by_id,
    update_review, delete_review
)

api = ReviewDTO.api
review_request = ReviewDTO.review_request
review_response = ReviewDTO.review_response

@api.route('/')
class ReviewList(Resource):
    @api.marshal_list_with(review_response)
    def get(self):
        """Get all reviews"""
        return get_all_reviews()

    @api.expect(review_request, validate=True)
    @api.marshal_with(review_response)
    def post(self):
        """Create a new review"""
        data = request.json
        return create_review(data)

@api.route('/<int:review_id>')
@api.param('review_id', 'The Review ID')
class ReviewResource(Resource):
    @api.marshal_with(review_response)
    def get(self, review_id):
        """Get review by ID"""
        return get_review_by_id(review_id)

    @api.expect(review_request, validate=True)
    @api.marshal_with(review_response)
    def put(self, review_id):
        """Update a review"""
        data = request.json
        return update_review(review_id, data)

    def delete(self, review_id):
        """Delete a review"""
        return delete_review(review_id)
