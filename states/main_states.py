from aiogram.dispatcher.filters.state import State, StatesGroup

class Product(StatesGroup):
    menu = State()
    product = State()

class Register(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    first_name = State()
    city = State()
    address = State()

class Banner(StatesGroup):
    menu = State()
    send = State()

class Lesson(StatesGroup):
    lessons = State()

class Company(StatesGroup):
    about = State()