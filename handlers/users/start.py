from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.keyboards import menu_keyboard, btn, back
from keyboards.inline.inline_keyboards import banner_inline_keyboard
from states.main_states import Product, Banner, Company, Lesson
from .product import product_menu
from .company import about_company_text
from .lesson import inline_keyboard, previous_or_next, get_data

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    full_name = message.chat.full_name
    user_name = message.chat.username
    telegram_id = message.chat.id
    await db.set_member(full_name, telegram_id, user_name)
    menu = await menu_keyboard()
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=menu)

@dp.message_handler()
async def bot_menu(msg: types.Message):
    text = msg.text
    if text == "Maxsulotlar🛍":
        await product_menu(msg=msg, state=FSMContext)

    elif text == "Marketing va imkoniyatlar📚":
        lessons = await db.get_lesson()
        button = await inline_keyboard(lessons['results'])
        data = lessons['results']
        text = "Darslar ro'yxati"
        for i in range(len(data)):
            text += f"\n{i+1}. {data[i]['name']}"
        await msg.answer("Darsliklar bo'limi", reply_markup=back)
        await msg.answer(text, reply_markup=button)
        await Lesson.lessons.set()
    elif text == "Korparatsiya haqidaℹ️":
        await about_company_text(msg, state=FSMContext)
        await Company.about.set()
    elif text == "Admin bo'lmi👤":
        is_admin = False
        for admin in ADMINS:
            if int(admin) == int(msg.chat.id):
                is_admin = True
        if is_admin:
            await msg.answer("Matin yuboring")
            await Banner.menu.set()
        else:
            await msg.answer("Bu menu faqat adminlar uchun")















