from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message
from loader import db
from data.config import ADMINS
cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Bekor qilish🚫")]
    ], resize_keyboard=True, row_width=2
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Ortga 🔙")]
    ], resize_keyboard=True
)

btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Ha"), KeyboardButton("Yo'q")],
        [KeyboardButton("Ortga 🔙")]
    ], resize_keyboard=True
)

async def category_keyboard():
    categories = await db.get_category()
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for category in categories:
        button.insert(KeyboardButton(category['name']))
    button.insert(KeyboardButton("Ortga 🔙"))
    return button

async def menu_keyboard(msg: Message):
    menu = [
        "Korparatsiya haqidaℹ️",
        "Maxsulotlar🛍",
        "Marketing va imkoniyatlar📚",
        "Natijalar 📊"
    ]
    button = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    is_admin =False
    for admin in ADMINS:
        if int(admin) == int(msg.chat.id):
            is_admin=True
    if is_admin:
        button.insert(KeyboardButton("Admin bo'lmi👤"))

    for item in menu:
        button.insert(
            KeyboardButton(item)
        )
    return button


async def product_menu_for_keyboard():
    button = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True, one_time_keyboard=True)
    button.insert(KeyboardButton("Telfon raqam📞", request_contact=True))
    button.insert(KeyboardButton("Bekor qilish🚫"))
    return button