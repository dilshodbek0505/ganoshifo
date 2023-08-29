from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.main_states import Register
from keyboards.default.keyboards import menu_keyboard, cancel, product_menu_for_keyboard
from keyboards.inline.inline_keyboards import region
from data.config import ADMINS

async def set_state_info(name, value, state: FSMContext):
    await state.update_data({
        name : value
    })

# foydalanuvchini bazaga saqlarsh
async def set_client(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')
    city = data.get('city')
    address = data.get('address')
    product = data.get('product')
    return await db.set_client(
        product=product,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        city=city,
        address=address,
    )

# barcha adminlarga xabar yuborish
async def send_message_all_admin(user,msg: types.Message, state: FSMContext):
    text = f"""
<b>Yangi buyurtma qabul qilindi.</b>

---------------
Mijoz haqida ma'lumot 👤
---------------

Ismi: <b>{user['first_name']}</b>
Familiyasi: <b>{user['last_name']}</b>
Viloyati: <b>{user['city']}</b>
Address: <b>{user['address']}</b>
Maxsulot nomi: <b>{user['product_id']['name']}</b>
Maxsulot idsi: <b>{user['product_id']['id']}</b>
"""
    for admin in ADMINS:
        await bot.send_message(admin, text)
    return True

# /start tugmasi bosilganda asosiy menuga qaytish
@dp.message_handler(commands=['start'], state=Register.all_states)
async def kick_state(msg: types.Message, state: FSMContext):
    button = await menu_keyboard(msg)
    await msg.delete()
    await msg.answer("Bosh menu", reply_markup=button)
    await state.finish()

# Bekor qilish🚫 tugamsi bosilganda amalni bekor qilish
async def cancel_fun(msg: types.Message, state: FSMContext):
    if msg.text == "Bekor qilish🚫":
        await kick_state(msg=msg, state=state)
        return True

# ism kiritish
@dp.message_handler(state=Register.first_name)
async def order_main_fun(msg: types.Message, state: FSMContext):
    if await cancel_fun(msg=msg, state=state):
        return True
    first_name = msg.text
    await set_state_info("first_name", first_name, state)
    await msg.delete()
    await msg.answer("Familiyangizni kriting: ")
    await Register.last_name.set()

# familiyani kiritish
@dp.message_handler(state=Register.last_name)
async def order_last_name(msg: types.Message, state: FSMContext):
    if await cancel_fun(msg=msg, state=state):
        return True
    last_name = msg.text
    await set_state_info('last_name', last_name, state)
    await msg.delete()
    button = await product_menu_for_keyboard()
    await msg.answer("Telfon raqamingizni kiriting", reply_markup=button)
    await Register.phone.set()

# telfon raqamni olish 1-yo'l
@dp.message_handler(content_types=types.ContentType.CONTACT, state=Register.phone)
async def order_phone_number_1(msg: types.Message, state: FSMContext):
    if await cancel_fun(msg=msg, state=state):
        return True
    phone = msg.contact.phone_number
    await set_state_info("phone", phone, state)
    await msg.delete()
    button = await region()
    # await msg.edit_reply_markup(reply_markup=cancel)
    # await msg.delete_reply_markup()
    await msg.answer("Viloatingizni tanlang", reply_markup=button)
    await Register.city.set()

# telgon raqami olish 2- yo'l
@dp.message_handler(content_types=types.ContentType.TEXT, state=Register.phone)
async def order_phone_number_2(msg: types.Message, state: FSMContext):
    if await cancel_fun(msg=msg, state=state):
        return True
    phone = msg.text
    await set_state_info("phone", phone, state)
    await msg.delete()
    button = await region()
    # await msg.edit_reply_markup(reply_markup=cancel)
    # await msg.delete_reply_markup()
    await msg.answer("Viloyatingizni tanlang", reply_markup=button)
    await Register.city.set()

# viloyatni olish
@dp.callback_query_handler(state=Register.city)
async def order_city_fun(cal: types.CallbackQuery, state: FSMContext):
    if await cancel_fun(msg=cal.message, state=state):
        return True
    data = cal.data
    await set_state_info("city", data, state)
    await cal.message.delete()
    await cal.message.answer("To'liq manzilingizni kiriting", reply_markup=cancel)
    await Register.address.set()
    await cal.answer(cache_time=0)

# to'liq manzilni olish
@dp.message_handler(state=Register.address)
async def order_address_fun(msg: types.Message, state: FSMContext):
    if await cancel_fun(msg=msg, state=state):
        return True
    await set_state_info("address", msg.text, state)
    user = await set_client(msg, state)
    send_message = await send_message_all_admin(user, msg, state)
    if send_message:
        await msg.answer("Buyurtma uchun raxmat!😊. Tez orada adminlarimiz siz bilan bog'lanishadi")
    await kick_state(msg,state)






