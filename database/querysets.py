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


# Questions
GET_ALL_QUESTIONS = """
    SELECT * FROM `questions`
"""

CREATE_NEW_QUESTION = """
    INSERT INTO `questions` (question, answer_options, true_answer)
    VALUES (?, ?, ?)
"""


# Answers
GET_ANSWERS_BY_SESSION_ID = """
    SELECT * FROM `answers`
    WHERE `session_id` == ?
"""


