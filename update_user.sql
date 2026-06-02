-- SQLite
-- Изменение имени пользователя
UPDATE users 
SET name = 'Алексей Смирнов (обновлён)', updated_at = CURRENT_TIMESTAMP
WHERE id = 1;