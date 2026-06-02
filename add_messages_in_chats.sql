-- SQLite
-- Очистка таблицы перед заполнением
DELETE FROM messages;

-- Сообщения в чате 1 (приватный чат) - 6 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(1, 1, 'Привет, Мария! Как дела?', datetime('now', '-5 days'), 0, 0),
(1, 2, 'Привет, Алексей! Хорошо, а у тебя?', datetime('now', '-5 days', '+2 minutes'), 0, 0),
(1, 1, 'Отлично! Как прошла встреча?', datetime('now', '-4 days'), 0, 0),
(1, 2, 'Всё хорошо, подписали документы', datetime('now', '-4 days', '+1 hour'), 0, 0),
(1, 1, 'Отличные новости! Поздравляю!', datetime('now', '-3 days'), 0, 0),
(1, 2, 'Спасибо! Завтра обсудим детали', datetime('now', '-2 days'), 0, 0);

-- Сообщения в чате 5 (Рабочий чат) - 14 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(5, 1, 'Коллеги, доброе утро!', datetime('now', '-3 days'), 0, 0),
(5, 2, 'Доброе утро!', datetime('now', '-3 days', '+5 minutes'), 0, 0),
(5, 3, 'Всем привет!', datetime('now', '-3 days', '+10 minutes'), 0, 0),
(5, 1, 'Напоминаю про созвон в 14:00', datetime('now', '-3 days', '+1 hour'), 0, 0),
(5, 4, 'Буду, подготовил отчёт', datetime('now', '-3 days', '+2 hours'), 0, 0),
(5, 5, 'Тоже буду, жду ссылку', datetime('now', '-3 days', '+3 hours'), 0, 0),
(5, 1, 'Ссылка на созвон: https://meet.example.com/123', datetime('now', '-2 days'), 0, 0),
(5, 2, 'Зашёл, всех ждём', datetime('now', '-2 days', '+30 minutes'), 0, 0),
(5, 6, 'Извините, опаздываю на 5 минут', datetime('now', '-2 days', '+45 minutes'), 0, 0),
(5, 3, 'Хороший созвон, всё обсудили', datetime('now', '-2 days', '+2 hours'), 0, 0),
(5, 1, 'Спасибо всем за участие!', datetime('now', '-2 days', '+3 hours'), 0, 0),
(5, 7, 'Когда следующий созвон?', datetime('now', '-1 days'), 0, 0),
(5, 1, 'В пятницу в то же время', datetime('now', '-1 days', '+10 minutes'), 0, 0),
(5, 8, 'Принято, готовлю материалы', datetime('now', '-1 days', '+30 minutes'), 0, 0);

-- Системное сообщение о присоединении
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(5, 9, 'Пользователь Павел Васильев присоединился к чату', datetime('now', '-6 days'), 1, 0);

-- Сообщения в чате 6 (Семья) - 6 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(6, 2, 'Семья, как планы на выходные?', datetime('now', '-4 days'), 0, 0),
(6, 1, 'Можем съездить за город', datetime('now', '-4 days', '+1 hour'), 0, 0),
(6, 3, 'Хорошая идея! Я с семьёй', datetime('now', '-4 days', '+2 hours'), 0, 0),
(6, 4, 'Тоже хочу! Какое место?', datetime('now', '-3 days'), 0, 0),
(6, 2, 'Предлагаю парк "Лесной"', datetime('now', '-3 days', '+1 hour'), 0, 0),
(6, 1, 'Во сколько встречаемся?', datetime('now', '-2 days'), 0, 0);

-- Сообщения в чате 7 (Друзья) - 6 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(7, 3, 'Ребята, кто пойдёт на футбол?', datetime('now', '-3 days'), 0, 0),
(7, 1, 'Я пойду, билеты уже купил', datetime('now', '-3 days', '+1 hour'), 0, 0),
(7, 2, 'Я тоже, какой сектор?', datetime('now', '-3 days', '+2 hours'), 0, 0),
(7, 3, 'Сектор B, места 15-20', datetime('now', '-3 days', '+3 hours'), 0, 0),
(7, 4, 'Записывайте меня в компанию', datetime('now', '-2 days'), 0, 0),
(7, 7, 'Тоже буду, созвонимся', datetime('now', '-2 days', '+1 hour'), 0, 0);

-- Сообщения в чате 8 (IT Сообщество) - 8 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(8, 1, 'Кто использует FastAPI в production?', datetime('now', '-5 days'), 0, 0),
(8, 2, 'Я использую, отличный фреймворк!', datetime('now', '-5 days', '+30 minutes'), 0, 0),
(8, 3, 'Тоже фанат FastAPI', datetime('now', '-5 days', '+1 hour'), 0, 0),
(8, 5, 'Какие есть минусы?', datetime('now', '-4 days'), 0, 0),
(8, 1, 'Минусов почти нет, но нужно понимать асинхронность', datetime('now', '-4 days', '+1 hour'), 0, 0),
(8, 7, 'Согласен, документация отличная', datetime('now', '-3 days'), 0, 0),
(8, 8, 'Перешёл с Django на FastAPI', datetime('now', '-3 days', '+2 hours'), 0, 0),
(8, 9, 'Как производительность?', datetime('now', '-2 days'), 0, 0);

-- Сообщения в чате 9 (Спорт) - 5 сообщений
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(9, 4, 'Кто смотрел вчерашний матч?', datetime('now', '-2 days'), 0, 0),
(9, 1, 'Да, отличная игра была', datetime('now', '-2 days', '+1 hour'), 0, 0),
(9, 5, 'Как вам судейство?', datetime('now', '-1 days'), 0, 0),
(9, 4, 'Следующий матч в субботу, погнали!', datetime('now', '-12 hours'), 0, 0),
(9, 6, 'Какой счёт?', datetime('now', '-10 hours'), 0, 0);

-- Сообщения в чате 10 (Путешествия) - 4 сообщения
INSERT INTO messages (room_id, sender_id, content, created_at, is_system, is_favorite) VALUES
(10, 5, 'Куда поедем этим летом?', datetime('now', '-3 days'), 0, 0),
(10, 2, 'Предлагаю горы', datetime('now', '-3 days', '+2 hours'), 0, 0),
(10, 3, 'Поддерживаю!', datetime('now', '-2 days'), 0, 0),
(10, 4, 'Когда планируем?', datetime('now', '-1 days'), 0, 0);