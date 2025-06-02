# controllers/enum_controller.py

from flask import Blueprint, jsonify
from app.main.utils.enums import CategoryName, StyleType

enum_bp = Blueprint('enum', __name__)

@enum_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify([e.value for e in CategoryName])

@enum_bp.route('/styles', methods=['GET'])
def get_styles():
    return jsonify([e.value for e in StyleType])
