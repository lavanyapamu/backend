from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def requires_role(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt_data = get_jwt()
            user_role = jwt_data.get("role")
            if user_role != role:
                return jsonify({"error": f"{role} access required"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
