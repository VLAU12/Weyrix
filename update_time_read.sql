-- SQLite
UPDATE chat_members 
SET last_read_at = CURRENT_TIMESTAMP 
WHERE room_id = 5 AND user_id = 1;