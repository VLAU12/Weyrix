--PRAGMA foreign_keys = ON;

-- ===== ШАГ 1: Создаем тестовые данные с уникальным временным штампом =====

-- 1. Создаем пользователя с уникальным user_tag
--INSERT INTO users (user_tag, name, hashed_password, email, created_at, updated_at)
--VALUES ('cascade_final_' || strftime('%s','now'), 'Cascade Final', 'hash_final', 'final_cascade@test.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Сохраняем ID пользователя
--SELECT last_insert_rowid() as user_id;

-- 2. Создаем чат
--INSERT INTO chat_rooms (created_by_id, is_private, is_active, created_at)
--VALUES (last_insert_rowid(), 0, 1, CURRENT_TIMESTAMP);

-- Сохраняем ID чата
--SELECT last_insert_rowid() as chat_room_id;

-- 3. Добавляем пользователя в чат
--INSERT INTO chat_members (room_id, user_id, joined_at, last_read_at, is_admin)
--VALUES (last_insert_rowid(), (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%'), 
--       CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1);

-- 4. Создаем сообщение
--INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite)
--VALUES ((SELECT id FROM chat_rooms WHERE created_by_id = (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%') LIMIT 1),
--        (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%'),
--        'Тестовое сообщение для CASCADE', 
--        CURRENT_TIMESTAMP, 0, 0);

-- ===== ШАГ 2: Проверяем данные перед удалением =====

--SELECT '=== ДАННЫЕ ДО УДАЛЕНИЯ ===' as '';

--SELECT '1. Пользователь:' as '';
--SELECT id, user_tag, name FROM users WHERE user_tag LIKE 'cascade_final_%';

--SELECT '2. Сообщения пользователя:' as '';
--SELECT id, sender_id, content FROM messages WHERE sender_id = (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%');

--SELECT '3. Участие в чатах:' as '';
--SELECT room_id, user_id, is_admin FROM chat_members WHERE user_id = (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%');

--SELECT '4. Чаты, созданные пользователем:' as '';
--SELECT id, created_by_id FROM chat_rooms WHERE created_by_id = (SELECT id FROM users WHERE user_tag LIKE 'cascade_final_%');

-- ===== ШАГ 3: Удаляем пользователя =====
--DELETE FROM users WHERE user_tag LIKE 'cascade_final_%';

-- ===== ШАГ 4: Проверяем результаты каскадного удаления =====

--SELECT '=== ДАННЫЕ ПОСЛЕ УДАЛЕНИЯ ===' as '';

--SELECT '1. Пользователь (должен отсутствовать):' as '';
--SELECT COUNT(*) as user_count FROM users WHERE user_tag LIKE 'cascade_final_%';

--SELECT '2. Сообщения (должны быть удалены - CASCADE):' as '';
--SELECT COUNT(*) as messages_remaining FROM messages WHERE sender_id = 10;

--SELECT '3. Участие в чатах (должно быть удалено - CASCADE):' as '';
--SELECT COUNT(*) as members_remaining FROM chat_members WHERE user_id = 10;

--SELECT '4. Чаты (created_by_id должен стать NULL - SET NULL):' as '';
--SELECT id, created_by_id FROM chat_rooms WHERE id = 17;

-- ===== ШАГ 5: Демонстрация ошибки FOREIGN KEY =====

--SELECT '=== ДЕМОНСТРАЦИЯ ОШИБОК FOREIGN KEY ===' as '';

-- Попытка создать сообщение от несуществующего пользователя
--INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite)
--VALUES (17, 99999, 'Сообщение от несуществующего пользователя', CURRENT_TIMESTAMP, 0, 0);

-- Попытка добавить в чат несуществующего пользователя
INSERT INTO chat_members (room_id, user_id, joined_at, last_read_at, is_admin)
VALUES (17, 99999, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0);