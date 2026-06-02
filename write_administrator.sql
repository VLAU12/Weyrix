-- SQLite
-- Назначение пользователя администратором в групповом чате
UPDATE chat_members 
SET is_admin = 1 
WHERE room_id = 5 AND user_id = 3;