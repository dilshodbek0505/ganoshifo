from aiogram import types
from loader import db, dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboards import product_inline_keyboard, for_product_inline_keyboard, region
from keyboards.default.keyboards import category_keyboard, menu_keyboard, cancel, back
from states.main_states import Product, Register
from data.config import ADMINS

#maxsulot qo'llanmasini yuborish
async def product_instruction(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product")
    product = await db.get_product(id=product_id)
    if product:
        instruction = product[0]['instruction']
        if instruction:
            instruction = instruction[0]
            file = instruction['file']
            if file:
                video = open(file[0]['file'], 'rb')
                await msg.answer_video(video, caption=instruction['description'])
            else:
                await msg.answer(instruction['description'])
        else:
            await msg.answer("Qo'llanma topilmadi")
    else:
        await msg.answer("Maxsulot topilmadi")


# kategoriyalar menunsini chiqarish
async def product_menu(msg: types.Message, state: FSMContext):
    """
    Kategoriyalar menusini chiqarish
    """
    button = await category_keyboard()
    await msg.answer("Kategoriyani tanlang", reply_markup=button)
    await Product.menu.set()

# kategoriya tanlanganda maxsulotlar ro'yxatini inline keyboar qilib qaytarish
async def category_button_fun(msg: types.Message, state: FSMContext):
    """
    Kategoriyaga tegishli maxsulotlari ro'yxatini chiqarish
    """

    category = msg.text
    product = await db.get_product(category=category)
    if product:
        button = await product_inline_keyboard(category)
        await msg.answer(f"{category} kategoriyasidagi maxsulotlar", reply_markup=button)
    else:
        await msg.answer("Maxsulot topilmadi")

# maxsulot haqida ma'lumot berish 
async def product_info_fun(cal: types.CallbackQuery, state: FSMContext):
    """
    Maxsulot haqida ma'lumot berish
    """

    product_id = cal.data
    await state.update_data({"product": product_id})
    product = await db.get_product(id=product_id)
    if product:
        button = await for_product_inline_keyboard()
        photo = None
        file = product[0]['file']
        if file:
            photo = open(file[0]["file"], 'rb')
        else:
            photo = open('images/image.jpg', 'rb')
        await cal.message.answer_photo(photo,product[0]['description'], reply_markup=button)
    else:
        await cal.message.answer("Maxsulot topilmadi")


# /start kammandasi kelganida bosh menuga o'tish
@dp.message_handler(commands=['start'], state=Product.all_states)
async def kick_state(msg: types.Message, state: FSMContext):
    button = await menu_keyboard()
    await msg.answer("Bosh menu", reply_markup=button)
    await state.finish()


@dp.message_handler(state=(Product.menu, Product.product))
async def product_menu_fun(msg: types.Message, state: FSMContext):
    if msg.text == "Ortga 🔙":
        await kick_state(msg=msg, state=state)
    else:
        await category_button_fun(msg=msg, state=state)

@dp.callback_query_handler(state=Product.menu)
async def product_inline_keyboard_fun(cal : types.CallbackQuery, state: FSMContext):
    await product_info_fun(cal=cal, state=state)
    await Product.product.set()
    await cal.answer(cache_time=0)

# buyurtma berish yoki qo'llanmani ko'rish
@dp.callback_query_handler(state=Product.product)
async def product_fun2(cal: types.CallbackQuery, state: FSMContext):
    txt = cal.data
    if txt == 'order':
        await cal.message.delete()
        await cal.message.answer("Ismingizni kiriting:", reply_markup=cancel)
        await Register.first_name.set()
    elif txt == "back":
        await cal.message.delete()
        await product_menu(msg=cal.message, state=state)
    elif txt == "instruction":
        await product_instruction(cal.message,state)
    await cal.answer(cache_time=0)



