# app/main/controllers/user_controller.py

from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.main.services.user import (
    get_all_users,
    get_user_by_id,
    update_user,
    soft_delete_user,
    change_password,
    update_contact
)

user_ns = Namespace("users", description="User operations")


@user_ns.route("")
class AllUsers(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        if claims.get("role") != "Admin":
            return {"error": "Admin only"}, 403

        return get_all_users(), 200


@user_ns.route("/<string:user_id>")
class UserById(Resource):
   @jwt_required()
   def get(self, user_id):
        identity = get_jwt_identity()
        current_user_id = str(identity['user_id'])
        current_user_role_id = identity['role_id']

        # If you need role name, look it up:
        role_name = None
        if current_user_role_id == 1:
            role_name = 'Admin'
        elif current_user_role_id == 2:
            role_name = 'Artist'
        else:
            role_name = 'User'

        user = get_user_by_id(current_user_id, user_id, role_name)
        if not user:
            return {"error": "Not found or unauthorized"}, 404
        print("📷 Backend sending image filename:", user.profile_image)
        return user.to_dict(), 200


   @jwt_required()
   def patch(self, user_id):
        return update_user(user_id, request.form, request.files)

   @jwt_required()
   def delete(self, user_id):
        current_user_id = str(get_jwt_identity())
        current_user_role = get_jwt().get("role")
        return soft_delete_user(current_user_id, user_id, current_user_role)


@user_ns.route("/<string:user_id>/change-password")
class UserChangePassword(Resource):
    @jwt_required()
    def patch(self, user_id):
        current_user_id = str(get_jwt_identity())
        if current_user_id != str(user_id):
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return {"error": "Missing fields"}, 400

        return change_password(user_id, old_password, new_password)


@user_ns.route("/<string:user_id>/update-contact")
class UserUpdateContact(Resource):
    @jwt_required()
    def patch(self, user_id):
        current_user_id = str(get_jwt_identity())
        if current_user_id != str(user_id):
            return {"error": "Unauthorized"}, 403

        data = request.get_json()
        email = data.get("email")
        phone_number = data.get("phone_number")

        return update_contact(user_id, email, phone_number)
