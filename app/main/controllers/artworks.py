from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from app.main.dto.artworks import ArtworkDTO
from app.main.services.artworks import (
    add_artwork,
    get_all_artworks,
    get_artwork_by_id,
    get_artworks_by_artist,
    update_artwork,
    soft_delete_artwork
)

artwork_ns = ArtworkDTO.api

@artwork_ns.route("")
class ArtworkList(Resource):
    @jwt_required()
    def post(self):
        
        artist_identity= get_jwt_identity()
        artist_id = artist_identity['user_id'] if isinstance(artist_identity, dict) else artist_identity
        data = {key: request.form.get(key, '') for key in request.form}             
        # request.form.to_dict()
        files = request.files
        return add_artwork(artist_id, data, files)

    def get(self):
        search = request.args.get("search")
        category = request.args.get("category")
        style = request.args.get("style")
        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")
        sort_by = request.args.get("sort_by")
        include_deleted = request.args.get("include_deleted", "false").lower() == "true"

        return get_all_artworks(
            search=search,
            category=category,
            style=style,
            min_price=min_price,
            max_price=max_price,
            sort_by=sort_by,
            include_deleted=include_deleted
        )

@artwork_ns.route("/<string:artwork_id>")
class ArtworkById(Resource):
    def get(self, artwork_id):
        return get_artwork_by_id(artwork_id)

    @jwt_required()
    def patch(self, artwork_id):
        artist_identity = get_jwt_identity()
        artist_id = artist_identity.get('user_id') if isinstance(artist_identity, dict) else artist_identity
        data = request.form.to_dict()
        files = request.files
        return update_artwork(artwork_id, artist_id, data, files)

    @jwt_required()
    def delete(self, artwork_id):
        artist_identity = get_jwt_identity()
        artist_id = artist_identity.get('user_id') if isinstance(artist_identity, dict) else artist_identity
        return soft_delete_artwork(artwork_id, artist_id)


@artwork_ns.route("/artist/<string:artist_id>")
class ArtworksByArtist(Resource):
    @cross_origin(origins="http://localhost:4200", supports_credentials=True)
    def get(self, artist_id):
        return get_artworks_by_artist(artist_id)
