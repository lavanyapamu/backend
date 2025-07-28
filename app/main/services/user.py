# app/main/services/user_service.py
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
import os

from flask import app, request
from app.main.models.user import User
from init_db import db, bcrypt


def get_all_users():
    users = User.query.filter_by(is_deleted=False).all()
    return [user.to_dict() for user in users]


def get_user_by_id(current_user_id, user_id, current_user_role):
    if current_user_role == 'Admin' or str(current_user_id) == str(user_id):
        user = User.query.get(user_id)
        if not user or user.is_deleted:
            return None
        return user.to_dict()
    return None


def update_user(user_id, data, files):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    profile_image = files.get('profile_image')
    if not user:
        return {"error": "User not found."}, 404

    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone_number' in data:
        user.phone_number = data['phone_number']
    if 'email' in data:
        user.email = data['email']
    if profile_image:
        filename = secure_filename(profile_image.filename)
        filepath = os.path.join('static/uploads', filename)
        try:
            profile_image.save(filepath)
            user.profile_image = filename  # Save filename only
        except Exception as e:
            print("Image save failed:", str(e))
            return {"error": "Failed to save image."}, 500

    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {"message": "Profile updated successfully."}, 200


def soft_delete_user(current_user_id, target_user_id, current_user_role):
    user = User.query.filter_by(user_id=target_user_id, is_deleted=False).first()
    if not user:
        return {"message": "User not found or already deleted"}, 404

    if current_user_role == "Admin" or current_user_id == target_user_id:
        user.is_deleted = True
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

    return {"message": "Unauthorized"}, 403


def change_password(user_id, old_password, new_password):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return {"error": "User not found."}, 404

    if not bcrypt.check_password_hash(user.password, old_password):
        return {"error": "Old password is incorrect."}, 400

    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {"message": "Password changed successfully."}, 200


def update_contact(user_id, email, phone_number):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return {"error": "User not found."}, 404

    if email:
        user.email = email
    if phone_number:
        user.phone_number = phone_number

    user.updated_at = datetime.now(timezone.utc)
    db.session.commit()

    return {"message": "Contact info updated successfully."}, 200
