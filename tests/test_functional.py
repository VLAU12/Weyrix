from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

# Тест 1: Регистрация нового пользователя
def test_register_user_success():
    # Используем уникальный email с timestamp
    import time
    unique_email = f"newuser_{int(time.time())}@example.com"
    
    response = client.post("/auth/register/", json={
        "email": unique_email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "New User"
    })
    assert response.status_code == 200
    assert "message" in response.json()

# Тест 2: Попытка регистрации с существующим email
def test_register_user_already_exists():
    email = "existing@example.com"
    
    # Первая регистрация
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "User"
    })
    
    # Вторая регистрация с тем же email
    response = client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "User"
    })
    assert response.status_code == 409

# Тест 3: Авторизация пользователя
def test_login_success():
    email = f"login_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "test12345",
        "password_check": "test12345",
        "name": "Login User"
    })
    
    response = client.post("/auth/login/", json={
        "email": email,
        "password": "test12345"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# Тест 4: Попытка входа с неверным паролем
def test_login_wrong_password():
    email = f"wrongpass_{int(time.time())}@example.com"
    
    client.post("/auth/register/", json={
        "email": email,
        "password": "correct123",
        "password_check": "correct123",
        "name": "Test User"
    })
    
    response = client.post("/auth/login/", json={
        "email": email,
        "password": "wrong123"
    })
    assert response.status_code == 401

# Тест 5: Получение главной страницы (лендинга)
def test_landing_page():
    response = client.get("/")
    assert response.status_code == 200
