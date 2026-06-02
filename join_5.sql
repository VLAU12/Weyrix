-- SQLite
-- Найти активные чаты (с сообщениями за последние 7 дней)
SELECT DISTINCT cr.id, cr.name, MAX(m.created_at) as last_message
FROM chat_rooms cr
INNER JOIN messages m ON cr.id = m.room_id
WHERE m.created_at > datetime('now', '-7 days')
GROUP BY cr.id, cr.name
ORDER BY last_message DESC;


