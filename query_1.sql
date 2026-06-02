-- SQLite
INSERT INTO users (user_tag, name, hashed_password, email, created_at, updated_at)
VALUES ('Wtest001', 'Alice', 'hash123', 'alice@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Результат: INSERT 1 0

-- 2. Пытаемся создать второго пользователя с тем же email
INSERT INTO users (user_tag, name, hashed_password, email, created_at, updated_at)
VALUES ('Wtest002', 'Bob', 'hash456', 'alice@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Результат: 
-- Error: UNIQUE constraint failed: users.email
-- Подробности: Пользователь с email 'alice@example.com' уже существует

-- 3. Создание пользователя с уникальным email — успешно
INSERT INTO users (user_tag, name, hashed_password, email, created_at, updated_at)
VALUES ('Wtest002', 'Bob', 'hash456', 'bob@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Результат: INSERT 1 0