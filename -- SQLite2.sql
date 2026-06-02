-- SQLite
-- Получение всех чатов с последними сообщениями
SELECT * FROM latest_messages_view 
ORDER BY last_message_time DESC;
