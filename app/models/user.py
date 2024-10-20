# user.py (models)

from app.models.initial_models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # This method allows the user object to be serialized and converted to JSON
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'created_at': self.created_at
        }
