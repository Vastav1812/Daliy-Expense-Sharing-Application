from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import get_user_expenses, update_user, delete_user
from app.controllers.expense_controller import get_overall_expenses

# Define a new blueprint to avoid naming conflicts
user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return get_user_expenses(user_id)

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    return update_user(user_id)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user(user_id)
