from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp, bot
from .product import kick_state
from states.main_states import Company
from keyboards.inline.inline_keyboards import company_for_keyboard


# kapaniya haqida matinli ma'lumot
async def about_company_text(msg: types.Message, state: FSMContext):
    company = await db.get_about()
    company = company[0]
    button = await company_for_keyboard()
    await msg.answer(company['description'], reply_markup=button)

# file nomidan kelib chiqab video yoki rasim ekanligini  aniqlash
async def image_or_video(file):
    image_format = ["jpeg","jpg", "png", "gif", "bmp", "tiff", "svg", 'webp']
    # video_format = ["mp4", "avi", "mkv", "mov", "wmv", "flv"]
    is_image = False
    for i in image_format:
        if f".{i}" in file:
            is_image = True
    return is_image

# kampaniya haqida vieoli va rasimli ma'lumotlar
async def about_company_file(msg: types.Message, state: FSMContext):
    company = await db.get_about()
    company = company[0]['file']
    for file in company:
        f = open(file, 'rb')
        is_image = await image_or_video(file)
        if is_image:
            await msg.answer_photo(f)
        else:
            await msg.answer_video(f)


@dp.callback_query_handler(state=Company.about)
async def company_about_fun(cal: types.CallbackQuery, state: FSMContext):
    data = cal.data
    if data == 'more':
        await about_company_file(cal.message, state)
    await kick_state(cal.message, state)
    await cal.answer(cache_time=0)