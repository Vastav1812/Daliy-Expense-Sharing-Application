import pytest

# Test User Registration (Using a unique email to avoid conflict)
def test_register_user(test_client):
    # Register a new user
    data = {
        "name": "Unique User",
        "email": "uniqueuser@example.com",  # Ensure this email is unique
        "password": "password123",
        "mobile": "9876543210"
    }
    response = test_client.post('/api/auth/register', json=data)
    
    # Check if the response is successful (Status 201)
    assert response.status_code == 201
    
    # Check if the token and user ID are in the response
    response_json = response.get_json()
    assert response_json['auth'] == True
    assert 'token' in response_json
    assert response_json['user']  # Ensure a valid user ID is returned

# Test User Login
def test_login_user(test_client):
    # Use the credentials of an already registered user
    data = {
        "email": "uniqueuser@example.com",  # Use the email from the registration test
        "password": "password123"
    }
    response = test_client.post('/api/auth/login', json=data)
    
    # Check if the response is successful (Status 200)
    assert response.status_code == 200
    
    # Check if the token is in the response
    response_json = response.get_json()
    assert response_json['auth'] == True
    assert 'token' in response_json

# Teardown: Optional step to delete the user after the test (if needed)
def test_cleanup_user(test_client):
    # Perform cleanup logic if needed (e.g., delete the test user)
    pass
