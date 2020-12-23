from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup


# ReplyMarkup
greet_kb = ReplyKeyboardMarkup()
button_hi = KeyboardButton('Привет :)')
greet_kb.add(button_hi)

greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

greet_kb3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

button_1 = KeyboardButton('1️⃣')
button_2 = KeyboardButton('2️⃣')
button_3 = KeyboardButton('3️⃣')

markup4 = ReplyKeyboardMarkup().add(button_1).add(button_2).add(button_3)

markup5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_1, button_2, button_3)

markup6 = ReplyKeyboardMarkup().row(button_1, button_2, button_3).add(button_hi)


# InlineMarkup
inline_kb1 = InlineKeyboardMarkup()
inline_button_1 = InlineKeyboardButton("Моя кнопка", callback_data='button_1')
inline_kb1.add(inline_button_1)
