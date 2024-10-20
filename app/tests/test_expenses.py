import pytest
from flask_jwt_extended import create_access_token

def test_create_expense(test_client):
    # Simulate a user with an access token
    token = create_access_token(identity=1)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test the creation of an expense
    data = {
        "description": "Lunch",
        "total_amount": 300,
        "split_method": "equal",
        "created_by": 1,
        "splits": [
            {"user_id": 1, "amount_owed": 150},
            {"user_id": 2, "amount_owed": 150}
        ]
    }
    response = test_client.post('/api/expenses/', json=data, headers=headers)
    assert response.status_code == 201
    assert b"Expense added successfully!" in response.data


def test_invalid_expense_creation(test_client):
    # Simulate a user with an access token
    token = create_access_token(identity=1)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test invalid expense creation with missing fields
    data = {
        "description": "Lunch"
    }
    response = test_client.post('/api/expenses/', json=data, headers=headers)
    assert response.status_code == 400


def test_overall_expenses(test_client):
    # Simulate a user with an access token
    token = create_access_token(identity=1)
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Test overall expenses retrieval
    response = test_client.get('/api/expenses/overall', headers=headers)
    assert response.status_code == 200
