import pytest
from app.users.auth import get_password_hash, verify_password, create_access_token
from app.users.schemas import SUserRegister
from app.users.models import generate_user_tag
from jose import jwt
from app.config import get_auth_data
from pydantic import ValidationError

# Тест 1: Проверка хэширования пароля
def test_password_hashing():
    password = "test_password_123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert isinstance(hashed, str)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

# Тест 2: Проверка создания JWT-токена
def test_create_access_token():
    user_id = "test_user_123"
    token = create_access_token({"sub": user_id})
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = jwt.decode(token, get_auth_data()['secret_key'], algorithms=['HS256'])
    assert payload['sub'] == user_id
    assert 'exp' in payload

# Тест 3: Проверка валидации данных пользователя
def test_user_register_validation():
    valid_data = {
        "email": "test@example.com",
        "password": "12345",
        "password_check": "12345",
        "name": "Test User"
    }
    user = SUserRegister(**valid_data)
    assert user.email == "test@example.com"
    
    invalid_data = {
        "email": "not_an_email",
        "password": "12345",
        "password_check": "12345",
        "name": "Test User"
    }
    with pytest.raises(ValidationError):
        SUserRegister(**invalid_data)

# Тест 4: Проверка генерации уникального user_tag
def test_generate_user_tag():
    tag1 = generate_user_tag()
    tag2 = generate_user_tag()
    
    assert len(tag1) == 9
    assert tag1[0] == 'W'
    assert tag1 != tag2
    assert all(c.islower() or c.isdigit() for c in tag1[1:])

# Тест 5: Проверка требований к длине пароля
def test_password_length_validation():
    # Пароль короче 5 символов должен вызывать ошибку
    invalid_data = {
        "email": "test@example.com",
        "password": "12",
        "password_check": "12",
        "name": "Test User"
    }
    with pytest.raises(ValidationError):
        SUserRegister(**invalid_data)
    
    # Пароль длиннее 50 символов должен вызывать ошибку
    long_password = "a" * 51
    invalid_data2 = {
        "email": "test@example.com",
        "password": long_password,
        "password_check": long_password,
        "name": "Test User"
    }
    with pytest.raises(ValidationError):
        SUserRegister(**invalid_data2)
