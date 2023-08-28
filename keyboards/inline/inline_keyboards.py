from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db

async def yes_or_no():
    button = InlineKeyboardMarkup(row_width=2)
    button.insert(InlineKeyboardButton(text="Ha", callback_data="yes"))
    button.insert(InlineKeyboardButton(text="Yo'q", callback_data="no"))
    return button

async def company_for_keyboard():
    button = InlineKeyboardMarkup(row_width=2)
    button.insert(InlineKeyboardButton(text="Ko'proq bilish ⇣", callback_data="more"))
    button.insert(InlineKeyboardButton(text="Ortga 🔙", callback_data="back"))
    return button

async def banner_inline_keyboard():
    button = InlineKeyboardMarkup(row_width=1)
    banners = await db.get_banner()
    for banner in banners:
        button.insert(
            InlineKeyboardButton(text=banner['name'], callback_data=banner['name'])
        )
    return button

async def region():
    city = (
        ("Toshkent shahar", "Toshkent shahar"),
        ("Toshkent viloyati", "Toshkent viloyati"),
        ("Andijon", "Andijon"),
        ("Buxoro", "Buxoro"),
        ("Farg'ona", "Farg'ona"),
        ("Jizzax", "Jizzax"),
        ("Xorazm", "Xorazm"),
        ("Namangan", "Namangan"),
        ("Navoiy", "Navoiy"),
        ("Qashqadaryo", "Qashqadaryo"),
        ("Surxandaryo", "Surxandaryo"),
        ("Sirdaryo", "Sirdaryo"),
        ("Samarqand", "Samarqand"),
        ("Qoraqalpog'istion Respublikasi", "Qoraqalpog'istion Respublikasi"),
    )
    button = InlineKeyboardMarkup(row_width=1)
    for item in city:
        button.insert(InlineKeyboardButton(text=item[0], callback_data=item[1]))
    return button

async def product_inline_keyboard(category):
    button = InlineKeyboardMarkup(row_width=2)
    products = await db.get_product(category= category)
    for product in products:
        button.insert(
            InlineKeyboardButton(text=product['name'], callback_data=product['id'])
        )
    return button

async def for_product_inline_keyboard():
    texts = [
        {
            "text": "Buyurtma berish🛒",
            "query": "order"
        },
        {
            "text": "Qo'llanma📒",
            "query": "instruction"
        },
        {
            "text": "Ortga 🔙",
            "query": "back"
        }
    ]
    button = InlineKeyboardMarkup(row_width=2)
    for text in texts:
        button.insert(
            InlineKeyboardButton(text=text['text'], callback_data=text['query'])
        )
    return button


