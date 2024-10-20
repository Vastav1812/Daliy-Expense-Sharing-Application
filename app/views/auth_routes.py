from flask import Blueprint
from app.controllers.auth_controller import register_user, login_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    print("Inside register route")  # Debugging statement
    return register_user()  # No arguments needed

@auth_bp.route('/login', methods=['POST'])
def login():
    print("Inside login route")  # Debugging statement
    return login_user()  # No arguments needed
