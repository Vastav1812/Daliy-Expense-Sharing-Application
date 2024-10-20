from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # Import JWTManager
from app.config import Config
from app.models.initial_models import db  
from app.models.user import User # Import your User model
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize db with the app
    
    # Initialize JWT Manager
    jwt = JWTManager(app)
    

    # Register blueprints
    from app.views.auth_routes import auth_bp
    from app.views.user_routes import user_bp
    from app.views.expense_routes import expense_bp
    from app.views.home_routes import home_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    print("User blueprint registered with '/api/users'")
    app.register_blueprint(expense_bp, url_prefix='/api/expenses')
    app.register_blueprint(home_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
