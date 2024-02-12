from aiogram.fsm.state import StatesGroup, State


class StepsQuiz(StatesGroup):
    GET_QUESTION = State()
    SAVE_ANSWER = State()
    END_GAME = State()
    CHOICE_SESSION = State()

