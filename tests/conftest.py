import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, Base
from sqlalchemy import text

@pytest.fixture(scope="function")
def client():
    """Фикстура для тестового клиента FastAPI с очисткой БД"""
    # Очищаем базу данных перед каждым тестом
    with engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
        Base.metadata.drop_all(conn)
        Base.metadata.create_all(conn)
    
    yield TestClient(app)
    
    # Очищаем после теста
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)

@pytest.fixture(scope="function")
def authenticated_client(client):
    """Фикстура для авторизованного клиента"""
    # Регистрируем пользователя
    client.post("/auth/register/", json={
        "email": "test@example.com",
        "password": "test12345",
        "password_check": "test12345",
        "name": "Test User"
    })
    
    # Входим в систему
    client.post("/auth/login/", json={
        "email": "test@example.com",
        "password": "test12345"
    })
    
    return client
