
from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from flask_restx import Resource
from app.main.dto.user import UserDTO
from app.main.services.user import (

    get_all_users,
    get_user_by_id,
    update_user,
    soft_delete_user
)
from app.main.utils.authorize import requires_role

user_ns = UserDTO.api


# @user_endpoint.route("/register")
# class Register(Resource):
#     def post(self):
#         data = request.get_json()
#         return register_user(data)


@user_ns.route("")
class AllUsers(Resource):
    @jwt_required()
    @requires_role("Admin")
    def get(self):
        return get_all_users()


@user_ns.route("/<string:user_id>")
class UserById(Resource):
    # def options(self, user_id):
    #     return '', 204
    @jwt_required()
    def get(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user_role = get_jwt().get("role")
        return get_user_by_id(current_user_id, user_id, current_user_role)

    @jwt_required()
    def patch(self, user_id):
        data = request.form.to_dict()
        files = request.files
        return update_user(user_id, data, files)

    @jwt_required()
    def delete(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user_role = get_jwt().get("role")
        return soft_delete_user(current_user_id, user_id, current_user_role)
