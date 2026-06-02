import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_favorites_chat_created_after_registration():
    email = f"favorites_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "Favorites User"
    })
    
    client.post("/auth/login/", json={
        "email": email,
        "password": "test12345"
    })
    
    response = client.get("/chat/chats")
    assert response.status_code == 200
    
    chats = response.json()
    favorites_exists = any(chat.get('name') == 'Избранное' for chat in chats)
    assert favorites_exists is True

def test_create_private_chat():
    email1 = f"user1_{int(time.time())}@example.com"
    email2 = f"user2_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email1,
        "password": "test12345",
        "password_check": "test12345",
        "name": "User One"
    })
    client.post("/auth/register/", json={
        "email": email2,
        "password": "test12345",
        "password_check": "test12345",
        "name": "User Two"
    })
    
    client.post("/auth/login/", json={
        "email": email1,
        "password": "test12345"
    })
    
    users_response = client.get("/auth/users")
    assert users_response.status_code == 200

def test_update_user_name():
    email = f"updatename_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "Original Name"
    })
    
    client.post("/auth/login/", json={
        "email": email,
        "password": "test12345"
    })
    
    response = client.post("/auth/update_name/", json={
        "name": "Updated Name"
    })
    assert response.status_code == 200

def test_logout():
    email = f"logout_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "Logout User"
    })
    
    client.post("/auth/login/", json={
        "email": email,
        "password": "test12345"
    })
    
    response = client.post("/auth/logout/")
    assert response.status_code == 200

def test_create_group_chat():
    email = f"group_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "Group Creator"
    })
    
    client.post("/auth/login/", json={
        "email": email,
        "password": "test12345"
    })
    
    response = client.post("/chat/groups/create/", json={
        "name": "Test Group",
        "description": "This is a test group"
    })
    
    assert response.status_code == 200
    assert "id" in response.json()
