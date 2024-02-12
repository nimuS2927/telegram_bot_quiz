# Users
INSERT_USER = """
    INSERT OR IGNORE INTO `users` (`telegram_id`, `first_name`, `last_name`)
    VALUES (?, ?, ?)
"""


# Sessions
GET_SESSION_BY_ID = """
    SELECT *
     FROM `sessions`
     WHERE `session_id` = ?
"""

GET_ACTIVE_SESSION = """
    SELECT *
     FROM `sessions`
     WHERE `user_id` = ? AND `status` = 0
"""

GET_OLD_SESSION = """
    SELECT `session_id`
     FROM `sessions`
     WHERE `time_last_answer` < ?
"""

CREATE_SESSION = """
    INSERT INTO `sessions` (user_id)
    VALUES (?)
"""

UPDATE_SESSION_STATUS = """
    UPDATE `sessions`
    SET `status` = ?
    WHERE `session_id` = ?
"""

UPDATE_SESSION_LAST_ANSWER = """
    UPDATE `sessions`
    SET `time_last_answer` = ?
    WHERE `session_id` = ?
"""

# Questions
GET_ALL_QUESTIONS = """
    SELECT * FROM `questions`
"""

GET_QUESTIONS_IF_NOT_ID = """
    SELECT * FROM `questions`
    WHERE `question_id` NOT IN (
    SELECT `question_id` FROM `answers`
    WHERE `session_id` == ?
    )
"""

INSERT_NEW_QUESTION = """
    INSERT INTO `questions` (question, answer_options, true_answer)
    VALUES (?, ?, ?)
"""


# Answers
GET_ANSWERS_BY_SESSION_ID = """
    SELECT * FROM `answers`
    WHERE `session_id` == ?
"""

INSERT_ANSWER = """
    INSERT INTO `answers` (question_id, session_id, answer, result)
    VALUES (?, ?, ?, ?)
"""



