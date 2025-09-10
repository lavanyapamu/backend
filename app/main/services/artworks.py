from datetime import datetime, timezone
import uuid
from app.main.models.artworks import Artwork
from app.main.utils.enums import CategoryName, StyleType, Orderstatus

from app.main.models.user import User

from init_db import db
from sqlalchemy import or_, asc, desc
from werkzeug.utils import secure_filename
import os
from flask import request



UPLOAD_FOLDER = '/home/lavanya/Desktop/ArtFlare/static/uploads' 

def add_artwork(artist_id, data, files):
    required_fields = ['title', 'description', 'category_name', 'style', 'price', 'quantity']
    missing = [field for field in required_fields if not data.get(field)]

    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400

    # Handle image
    image = files.get('art_image')
    if not image:
        return {"error": "No image provided"}, 400

    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        image.save(image_path)
    except Exception as e:
        return {"error": f"Failed to save image: {str(e)}"}, 500

    try:
        # Handle Enum safely
        try:
            category = CategoryName[data['category_name'].lower()]
            category_value = category.value
            style = StyleType[data['style'].lower()]
        except KeyError:
            return {"error": "Invalid category or style name."}, 400

        print(image_path)
        new_artwork = Artwork(  
            artist_id=artist_id,
            title=data['title'],
            description=data['description'],
            category_name=category_value,
            style=style,
            price=float(data['price']),
            quantity=int(data['quantity']),
            art_image=filename,  # Save image path, not binary
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        print(category.value)

        print(filename)
        db.session.add(new_artwork)
        db.session.commit()
        print("came here")

        return {
            "message": "Artwork added successfully",
            "artwork_id": str(new_artwork.artwork_id)
        }, 201

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to add artwork: {str(e)}"}, 500

def get_all_artworks(
    search=None,
    category=None,
    style=None,
    min_price=None,
    max_price=None,
    sort_by=None,
    include_deleted=False
):
    query = Artwork.query

    if not include_deleted:
        query = query.filter_by(is_deleted=False)

    if category:
        query = query.filter(Artwork.category_name == CategoryName[category.lower()])
    if style:
        query = query.filter(Artwork.style == StyleType[style.lower()])
    if min_price is not None:
        query = query.filter(Artwork.price >= float(min_price))
    if max_price is not None:
        query = query.filter(Artwork.price <= float(max_price))

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                Artwork.title.ilike(search_term),
                Artwork.description.ilike(search_term)
            )
        )

    if sort_by == "price_asc":
        query = query.order_by(asc(Artwork.price))
    elif sort_by == "price_desc":
        query = query.order_by(desc(Artwork.price))
    elif sort_by == "newest":
        query = query.order_by(desc(Artwork.created_at))
    elif sort_by == "popular":
        query = query.order_by(desc(Artwork.sales_count))

    artworks = query.all()
    return [art.to_dict() for art in artworks], 200


def get_artwork_by_id(artwork_id):
    artwork = Artwork.query.filter_by(artwork_id=artwork_id, is_deleted=False).first()
    if not artwork:
        return {"error": "Artwork not found"}, 404
    return artwork.to_dict(), 200


def update_artwork(artwork_id, artist_id, data, files):
    artwork = Artwork.query.filter_by(artwork_id=artwork_id, artist_id=artist_id, is_deleted=False).first()
    if not artwork:
        return {"error": "Artwork not found or unauthorized"}, 404

    try:
        if 'title' in data:
            artwork.title = data['title']
        if 'description' in data:
            artwork.description = data['description']
        if 'category_name' in data:
            artwork.category_name = CategoryName[data['category_name'].lower()]
        if 'style' in data:
            artwork.style = StyleType[data['style'].lower()]
        if 'price' in data:
            artwork.price = float(data['price'])
        if 'quantity' in data:
            artwork.quantity = int(data['quantity'])

        if 'art_image' in files:
            image_file = files['art_image']
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join('/home/lavanya/Desktop/ARTFLARE/frontend/public/artworks', filename))  # update path
            artwork.art_image = filename

        artwork.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return {"message": "Artwork updated successfully"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update artwork: {str(e)}"}, 500


def soft_delete_artwork(artwork_id, artist_id):
    artwork = Artwork.query.filter_by(artwork_id=artwork_id, artist_id=artist_id, is_deleted=False).first()
    if not artwork:
        return {"error": "Artwork not found or unauthorized"}, 404

    try:
        artwork.is_deleted = True
        db.session.commit()
        return {"message": "Artwork soft deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete artwork: {str(e)}"}, 500


def get_artworks_by_artist(artist_id):
    try:
        artist_id = uuid.UUID(artist_id)   
    except ValueError:
        return {"error": "Invalid artist_id"}, 400
    artworks= Artwork.query.filter_by(artist_id=artist_id, is_deleted=False).all()

    return [a.to_dict() for a in artworks], 200
   
def get_filters():
    return {
        "categories": [c.value for c in CategoryName],
        "styles": [s.value for s in StyleType],
        "statuses": [s.value for s in Orderstatus] 
    }, 200