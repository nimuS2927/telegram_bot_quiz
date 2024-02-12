from json import dumps
from typing import Dict
from random import randint, shuffle
from datetime import datetime

from aiogram import F
from aiogram import types, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from core.keyboards.reply import \
    get_start_game_keyboard, \
    get_confirm_keyboard, \
    get_choice_keyboard
from core.utils.statesquiz import StepsQuiz
from core.utils.excel_to_json import DELIMITER_ANSWER_OPTIONS

from config import PATH_TO_DATABASE, MAX_COUNT_QUESTIONS_IN_QUIZ

from database.db_work import get_info_from_db, insert_info_to_db, update_info_from_db
from database.querysets import \
    GET_ACTIVE_SESSION, \
    GET_ALL_QUESTIONS, \
    INSERT_ANSWER, \
    CREATE_SESSION, \
    GET_ANSWERS_BY_SESSION_ID, \
    UPDATE_SESSION_STATUS, \
    GET_QUESTIONS_IF_NOT_ID, \
    INSERT_USER, UPDATE_SESSION_LAST_ANSWER


async def cmd_start(message: types.Message):
    await message.answer(f"Данный бот проведет для вас Квиз на тему программирования!",
                         reply_markup=get_start_game_keyboard())
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await insert_info_to_db(INSERT_USER, user_id, first_name, last_name)


async def new_game(message, state, user_id):
    id_session = await insert_info_to_db(CREATE_SESSION, user_id)
    data = await get_info_from_db(GET_ALL_QUESTIONS)
    await state.update_data(questions=data, id_session=id_session[0])
    await state.set_state(StepsQuiz.GET_QUESTION)
    await cmd_game(message, state)


async def cmd_quiz(message: types.Message, state: FSMContext):
    await message.answer(f"Давайте начнем квиз!")
    user_id = message.from_user.id
    active_session = await get_info_from_db(GET_ACTIVE_SESSION, user_id)
    if len(active_session) == 0:
        # Запустить новый квиз
        await new_game(message, state, user_id)
    else:
        # спросить запустить новый или продолжить старый квиз
        await message.answer(f"У вас сохранилась не заверщенная сессия, желаете продолжить?",
                             reply_markup=get_confirm_keyboard()
                             )
        await state.update_data(id_session=active_session[0][0])
        await state.set_state(StepsQuiz.CHOICE_SESSION)


async def choice_session(message: types.Message, state: FSMContext):
    choice = message.text
    user_id = message.from_user.id
    context_data = await state.get_data()
    id_session = context_data['id_session']
    if choice == 'Yes':
        # Продолжаем сессию
        questions = await get_info_from_db(GET_QUESTIONS_IF_NOT_ID, id_session)
        await state.update_data(questions=questions,
                                questions_count=len(MAX_COUNT_QUESTIONS_IN_QUIZ - questions))
        await state.set_state(StepsQuiz.GET_QUESTION)
        await cmd_game(message, state)
    else:
        # Запускаем новую сессию завершая прошлую
        await update_info_from_db(UPDATE_SESSION_STATUS, 1, id_session)
        await new_game(message, state, user_id)


async def cmd_game(
        message: types.Message,
        state: FSMContext
):
    # Получаем данные из машины состояний
    context_data = await state.get_data()
    questions = context_data.get('questions')  # список вопросов
    questions_count = context_data.get('questions_count')  # количество заданных вопросов в текущей сессии
    # Если вопросов не осталось, останавливаем квиз
    # Если было задано MAX_COUNT_QUESTIONS_IN_QUIZ вопросов, останавливаем квиз
    if len(questions) == 0 or questions_count == MAX_COUNT_QUESTIONS_IN_QUIZ:
        await message.answer(f'Квиз окончен')
        await state.set_state(StepsQuiz.END_GAME)
        await cmd_end_game(message, state)
        return
    user_id = message.from_user.id
    if not questions_count:
        questions_count = 0
    # получаем случайный индекс для выбора вопроса
    cur_question_index = randint(0, len(questions) - 1)
    question_data = questions[cur_question_index]
    question_id = question_data[0]
    question = question_data[1]  # Вопрос
    answer_options = question_data[2].split(DELIMITER_ANSWER_OPTIONS)  # Варианты ответов
    shuffle(answer_options)  # Перемешиваем спиок вариантов ответов
    true_answer = question_data[3]  # Правильный ответ
    # задаем вопрос и получаем на него ответ
    await message.answer(
        text=f'Вопрос {questions_count + 1}.{question}\n'
             f'1. {answer_options[0]}\n'
             f'2. {answer_options[1]}\n'
             f'3. {answer_options[2]}\n'
             f'4. {answer_options[3]}\n'
             f'Выберите один правильный вариант.',
        reply_markup=get_choice_keyboard()
    )
    await state.update_data(
        questions=questions,
        questions_count=questions_count,
        cur_question_index=cur_question_index,
        current_question_id=question_id,
        current_answer_options=answer_options,
        current_true_answer=true_answer
    )
    await state.set_state(StepsQuiz.SAVE_ANSWER)


async def cmd_save_answer(
        message: types.Message,
        state: FSMContext
):
    answer_index = message.text
    context_data = await state.get_data()

    questions = context_data['questions']
    id_session = context_data['id_session']
    questions_count = context_data['questions_count']
    cur_question_index = context_data['cur_question_index']
    question_id = context_data['current_question_id']
    answer_options = context_data['current_answer_options']
    true_answer = context_data['current_true_answer']
    # Удаляем вопрос из общего списка
    del questions[cur_question_index]
    questions_count += 1
    result = 1 if true_answer == answer_options[int(answer_index) - 1] else 0
    await insert_info_to_db(INSERT_ANSWER,
                            question_id,
                            id_session,
                            answer_options[int(answer_index) - 1],
                            result
                            )
    await state.update_data(
        questions=questions,
        questions_count=questions_count,
    )
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update_info_from_db(UPDATE_SESSION_LAST_ANSWER, current_datetime, id_session)
    await state.set_state(StepsQuiz.GET_QUESTION)
    await cmd_game(message, state)


async def cmd_end_game(
        message: types.Message,
        state: FSMContext
):
    context_data = await state.get_data()
    id_session = context_data['id_session']
    await update_info_from_db(UPDATE_SESSION_STATUS, 1, id_session)
    answers = await get_info_from_db(GET_ANSWERS_BY_SESSION_ID, id_session)
    valid_answer = 0
    for answer in answers:
        valid_answer += answer[4]
    await message.answer(f'Дано правильных ответов {valid_answer} из {len(answers)}')
    await state.clear()


# Удалить, сервисная команда
async def cmd_get_info_message(message: types.Message, bot: Bot):
    await message.answer(dumps(message.model_dump(), default=str))
