from flask_restx import Namespace, fields

class ReviewDTO:
    api = Namespace("reviews", description="reviews")

    # Add request model
    review_request = api.model('ReviewRequest', {
        'user_id': fields.String(required=True, description='User UUID'),
        'artwork_id': fields.String(required=True, description='Artwork UUID'),
        'rating': fields.Float(required=True, description='Rating value'),
        'review_text': fields.String(description='Review text', required=False)
    })

    # Add response model
    review_response = api.model('ReviewResponse', {
        'review_id': fields.Integer(description='Review ID'),
        'user_id': fields.String(description='User UUID'),
        'artwork_id': fields.String(description='Artwork UUID'),
        'rating': fields.Float(description='Rating value'),
        'review_text': fields.String(description='Review text'),
        'created_at': fields.DateTime(description='Creation timestamp'),
        'updated_at': fields.DateTime(description='Last update timestamp'),
    })
