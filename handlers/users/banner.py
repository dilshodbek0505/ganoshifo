from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp, bot
from keyboards.default.keyboards import back
from keyboards.inline.inline_keyboards import yes_or_no
from states.main_states import Banner
from .product import kick_state


@dp.message_handler(state=Banner.menu, content_types=types.ContentType.TEXT)
async def banner_menu(msg: types.Message, state: FSMContext):
    text = msg.text
    if text == "Ortga 🔙":
        await kick_state(msg, state)
    else:
        await state.update_data({
            "text": text
        })
        button = await yes_or_no()
        await msg.answer(text +  "\n\nXabarni barcha foydalanuvchilarga yuborishni tasdiqlang", reply_markup=button)

@dp.callback_query_handler(state=Banner.menu)
async def send_message(cal : types.CallbackQuery, state: FSMContext):
    data = cal.data
    if data == "yes":
        try:
            members = await db.get_member()
            state_data = await state.get_data()
            text = state_data.get("text")
            for member in members:
                await bot.send_message(member['telegram_id'], text)
            await cal.message.answer("Barcha foydalanuvchilarga xabar yetqazildi")
            await kick_state(cal.message, state)
        except:
            pass
    elif data == "no":
        await kick_state(cal.message, state)
    await cal.answer(cache_time=0)