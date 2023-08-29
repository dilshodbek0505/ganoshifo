from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db, dp, bot
from states.main_states import Lesson
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.default.keyboards import back
from .product import kick_state


# inline keyboardni tayyorlash
async def inline_keyboard(data):
    buttons = []
    for lesson in data:
        buttons.append([InlineKeyboardButton(text=lesson['name'], callback_data=lesson['id'])])
    buttons.append([InlineKeyboardButton(text='⬅️', callback_data='previous'),InlineKeyboardButton(text='➡️', callback_data='next')])
    keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=buttons)
    # print(keyboard)
    return keyboard

# darslar haida ma'lumotlarni olish
async def get_data(state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    # print(url)
    res = None
    if url != None:
        res = await db.get_lesson_next(url)
    else:
        res = await db.get_lesson()
        # print(res)
    await state.update_data({
            "next" : res['next'],
            "previous" : res['previous']
        })
    return res['results']

# previous yoki next ga qarab url qaytarish
async def previous_or_next(cal: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    previous = data.get("previous")
    next = data.get("next")
    if cal.data == 'next':
        await state.update_data({
            "url": next
        })
    elif cal.data == 'previous':
        await state.update_data({
            "url": previous
        })

# darslarni yuborish
async def send_lesson(cal: types.CallbackQuery, state: FSMContext):
    video_id = int(cal.data)
    lesson = await db.get_one_lesson(video_id)
    lesson = lesson['data']
    if lesson['file'] == []:
        await cal.message.answer(lesson['description'])
    else:
        file = open(lesson['file'][0]['file'], 'rb')
        await cal.message.answer_video(file, caption=lesson['description'])

# Ortga 🔙 yuborilganda bosh menuga qaytish
@dp.message_handler(state=Lesson.all_states)
async def back_home_menu(msg: types.Message, state: FSMContext):
    if msg.text == 'Ortga 🔙':
        await kick_state(msg, state)
    

#/start kammandasi bosilganda bosh menuga qaytish
@dp.message_handler(commands=['start'],state=Lesson.all_states)
async def lesson_back(msg: types.Message, state: FSMContext):

    await kick_state(msg, state)



@dp.callback_query_handler(state=Lesson.lessons)
async def lesson_main_menu(cal: types.CallbackQuery, state: FSMContext):
    if cal.data != 'next' and cal.data != 'previous':
        await send_lesson(cal, state)
    else:
        await previous_or_next(cal, state)
        data = await get_data(state)
        button = await inline_keyboard(data)
        await cal.message.delete()
        text = "Darslar ro'yxati"
        for i in range(len(data)):
            text += f"\n{i+1}. {data[i]['name']}"
        await cal.message.answer(text, reply_markup=button)
    await cal.answer(cache_time=0)


# # darsliklar ro'yxati
# async def lessons_button(data):
#     button = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
#     for lesson in data:
#         button.insert(KeyboardButton(lesson['name']))
#     button.insert(KeyboardButton(""))
#     button.insert(KeyboardButton(""))
#     return button

# # ma'lumot yuborish
# async def lesson_data(url: None, state: FSMContext):
#     if url == None:
#         data = await db.get_lesson()
#         await state.update_data({
#             "previous": data['previous'],
#             "next":  data[]
#         })