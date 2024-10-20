from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.models.initial_models import db

# Register a new user
def register_user():
    data = request.get_json()

    # Input validation
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Name, email, and password are required"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create new user
    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        mobile=data.get('mobile', None)
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT token
        access_token = create_access_token(identity=new_user.id)
        return jsonify({"auth": True, "token": access_token, "user": new_user.id}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred while creating the user", "details": str(e)}), 500

# Login user
def login_user():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"error": "No user found"}), 404

    # Check if password is valid
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({"auth": False, "token": None, "message": "Invalid password"}), 401

    # Generate JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({"auth": True, "token": access_token}), 200

# Logout user
def logout_user():
    return jsonify({"auth": False, "token": None}), 200

