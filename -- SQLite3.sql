-- SQLite
-- Создание представления для получения последнего сообщения в каждом чате
CREATE VIEW IF NOT EXISTS latest_messages_view AS
SELECT 
    cr.id AS room_id,
    cr.name AS room_name,
    cr.is_private,
    m.id AS last_message_id,
    m.content AS last_message_content,
    m.created_at AS last_message_time,
    u.name AS last_message_sender,
    u.user_tag AS last_message_sender_tag
FROM chat_rooms cr
LEFT JOIN messages m ON cr.id = m.room_id
LEFT JOIN users u ON m.sender_id = u.id
WHERE m.id IS NULL OR m.id = (
    SELECT id FROM messages 
    WHERE room_id = cr.id 
    ORDER BY created_at DESC 
    LIMIT 1
);
