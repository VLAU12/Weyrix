-- SQLite
-- Получение последних сообщений для пользователя с id = 1
SELECT lmv.*
FROM latest_messages_view lmv
INNER JOIN chat_members cm ON lmv.room_id = cm.room_id
WHERE cm.user_id = 1
ORDER BY lmv.last_message_time DESC;
