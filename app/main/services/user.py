from datetime import datetime, timezone
from flask import jsonify
from app.main.models.user import User
from app.main.models.roles import Role
# from app.main.models. import StatusEnum  # Enum: 'Pending', 'Approved', etc.
# from manage import bcrypt, db
from init_db import db
import base64

# def register_user(data):
#     required_fields = ['full_name', 'email', 'password', 'role']
#     missing_fields = [field for field in required_fields if not data.get(field)]
    
#     if missing_fields:
#         return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

#     if User.query.filter_by(email=data['email']).first():
#         return {"error": "Email already registered."}, 400

#     role_obj = Role.query.filter_by(name=data['role']).first()
#     if not role_obj:
#         return {"error": "Invalid role"}, 400

#     try:
#         hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

#         new_user = User(
#             full_name=data['full_name'],
#             email=data['email'],
#             phone_number=data.get('phone_number'),
#             password=hashed_password,
#             role_id=role_obj.role_id,
#             earnings=0.0 if role_obj.name == "Artist" else None,
#             status=StatusEnum.PENDING.value,
#             created_at=datetime.now(timezone.utc),
#             updated_at=datetime.now(timezone.utc)
#         )

#         db.session.add(new_user)
#         db.session.commit()

#         return {"message": "User registered successfully.", "user_id": str(new_user.user_id)}, 201

#     except Exception as e:
#         db.session.rollback()
#         return {"error": f"Registration failed: {str(e)}"}, 500


def get_all_users():
    users = User.query.filter_by(is_deleted=False).all()
    return [user.to_dict() for user in users], 200


def get_user_by_id(current_user_id, user_id, current_user_role):
    if current_user_role == 'Admin' or current_user_id == user_id:
        user = User.query.get(user_id)
        if not user or user.is_deleted:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
    return {"error": "Unauthorized access"}, 403


from flask import request
from datetime import datetime, timezone
# from app.main import db
from app.main.models.user import User

def update_user(user_id, data, files):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return {"error": "User not found."}, 404

    try:
        # Get data from form and file from request
        data = request.form
        files = request.files

        # Update fields if provided
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        if 'email' in data:
            user.email = data['email']
        if 'profile_image' in files:
            image_file = files['profile_image']
            user.profile_image = image_file.read()

        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return {"message": "Profile updated successfully."}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update profile: {str(e)}"}, 500



def soft_delete_user(current_user_id, target_user_id, current_user_role):
    user = User.query.filter_by(user_id=target_user_id, is_deleted=False).first()
    if not user:
        return {"message": "User not found or already deleted"}, 404

    if current_user_role == "Admin" or current_user_id == target_user_id:
        try:
            user.is_deleted = True
            db.session.commit()
            message = "User deleted successfully" if current_user_role == "Admin" else "Your account has been deleted"
            return {"message": message}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": "Failed to delete user"}, 500
    else:
        return {"message": "Unauthorized to delete this user"}, 403

