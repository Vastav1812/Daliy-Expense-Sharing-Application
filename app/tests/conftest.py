# tests/conftest.py
import pytest
from app.initiate_app import create_app  # Correct the import path
from app.models.initial_models import db

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()

    # Flask provides a way to test the app by using test_client()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()  # Create tables
            yield testing_client  # This is where the testing happens

            db.drop_all()  # Clean up the database after tests
