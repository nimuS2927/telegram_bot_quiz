PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS `users` (
    telegram_id INTEGER PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `sessions` (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    time_last_answer VARCHAR(30) DEFAULT NULL,
    count_answer INTEGER DEFAULT 0,
    status INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES `users` (telegram_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `questions` (
    question_id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    answer_options TEXT NOT NULL,
    true_answer TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS `answers` (
    answer_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    session_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    result INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES `questions` (question_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES `sessions` (session_id) ON DELETE CASCADE
);

