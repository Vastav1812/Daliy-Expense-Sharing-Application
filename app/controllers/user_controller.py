from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.initial_models import db
from app.models.expense import Expense

def get_user_expenses(user_id):
    # Fetch expenses for the user
    expenses = Expense.query.filter_by(user_id=user_id).all()
    if not expenses:
        return jsonify({"error": "No expenses found for this user"}), 404
    return jsonify([expense.serialize() for expense in expenses]), 200

# Get user by ID
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()

    # Only allow users to fetch their own data
    if current_user_id != user_id:
        return jsonify({"error": "You are not authorized to view this user"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.serialize()), 200

# Update user by ID
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    # Only allow users to update their own data
    if current_user_id != user_id:
        return jsonify({"error": "You are not authorized to update this user"}), 403

    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update user details
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.mobile = data.get('mobile', user.mobile)

    try:
        db.session.commit()
        return jsonify(user.serialize()), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while updating the user", "details": str(e)}), 500

# Delete user by ID
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()

    # Only allow users to delete their own data
    if current_user_id != user_id:
        return jsonify({"error": "You are not authorized to delete this user"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "An error occurred while deleting the user", "details": str(e)}), 500



