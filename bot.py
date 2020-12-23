from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode

from config import TOKEN
import requests

####

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import TestStates

from json import dump, load
import keyboards as kb

WEATHER_TOKEN = 'e7444caba5c079597539cba7f81adcd8'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={token}'


# Создание бота по токену
bot = Bot(token=TOKEN)
# dispatcher
# dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
###############


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply('Привет! Напиши мне что-нибудь!')


@dp.message_handler(commands=["hi1"])
async def hi1(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.greet_kb)


@dp.message_handler(commands=["hi2"])
async def hi2(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.greet_kb2)


@dp.message_handler(commands=["hi3"])
async def hi3(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.greet_kb3)


@dp.message_handler(commands=["hi4"])
async def hi4(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.markup4)

@dp.message_handler(commands=["hi5"])
async def hi5(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.markup5)

@dp.message_handler(commands=["hi6"])
async def hi6(message: types.Message):
    await message.reply('Нажми на кнопку!', reply_markup=kb.markup6)

@dp.message_handler(commands=["in1"])
async def in1(message: types.Message):
    await message.reply('Моя первая инлайн кнопка!', reply_markup=kb.inline_kb1)

@dp.message_handler(commands=["weather"])
async def weather(message: types.Message):
    await message.reply('Узнайте погоду в городах:', reply_markup=kb.inline_kb2)


@dp.callback_query_handler(lambda c: c.data == 'button_1')
async def inline_b1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата любимая кнопка!!')


@dp.callback_query_handler(lambda c: c.data.startswith('weather'))
async def inline_weather(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    city = callback_query.data.split('=')[-1]
    api_link = WEATHER_URL.format(city_name=city, token=WEATHER_TOKEN)
    data = requests.get(url=api_link)
    print(data.json())
    kelvin = 273.15
    temperature = data.json()['main']['temp'] - kelvin
    feels_like = data.json()['main']['feels_like'] - kelvin
    await bot.send_message(callback_query.from_user.id,
                           f'Погода в {city} -> ({int(temperature)}), но ощущается как ({int(feels_like)})!')


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply('Слушаюсь и повинуюсь!')
    await bot.send_message(message.from_user.id, """
Доступные команды:
/start,
/help,
/photo,
/setstate,
/exam,
/hi1,
/hi2,
/hi3,
/hi4,
/hi5,
/hi6,
/in1,
/weather
    """)


@dp.message_handler(commands=["photo"])
async def photo_reply(message: types.Message):
    link = 'https://icatcare.org/app/uploads/2019/03/caring-for-your-cats-eyes-1.png'
    caption = 'Какие глаза!!! :eyes:'
    await bot.send_photo(message.from_user.id, link, caption=emojize(caption))


# @dp.message_handler(state="*", commands=["setstate"])
# async def process_setstate(message: types.Message):
#     argument = message.get_args()
#     state = dp.current_state(user=message.from_user.id)
#     if not argument:  # пустой аргумент
#         await state.reset_state()
#         return await message.reply('Состояние успешно сброшено')
#
#     if (not argument.isdigit()) or (int(argument) >= len(TestStates.all())):
#         return await message.reply(f"Ключ {argument} не подходит")
#
#     await state.set_state(TestStates.all()[int(argument)])
#     await message.reply('Текущее состояние успешно изменено', reply=False)


# @dp.message_handler(state=TestStates.TEST_STATE_0)
# async def state0(message: types.Message):
#     print(TestStates.TEST_STATE_0)
#     await message.reply('First stage!!1', reply=False)
#
#
# @dp.message_handler(state=TestStates.TEST_STATE_1[0])
# async def state2(message: types.Message):
#     await message.reply('Second stage!!1', reply=False)
#
#
# @dp.message_handler(state=TestStates.TEST_STATE_4 | TestStates.TEST_STATE_5)
# async def state45(message: types.Message):
#     await message.reply('Forth or fifth stage!!1', reply=False)
#

@dp.message_handler(state="*", commands=["setstate"])
async def process_setstate(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    return await message.reply('Состояние успешно сброшено')


def file_fill(user_id, data=None):
    print(data)
    if not data:
        data = {
            "age": "",
            "name": "",
            "hobby": "",
        }
    with open(f'user_data/{user_id}.json', 'w', encoding='utf-8') as file:
        dump(data, file)

@dp.message_handler(state="*", commands=["exam"])
async def start(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[0])
    await message.reply('Начнем опрос!', reply=False)
    await message.reply('Напишите Ваше имя!', reply=False)
    file_fill(message.from_user.id)

def change_user_file(user_id, field, content: str):
    with open(f'user_data/{user_id}.json', 'r', encoding='utf-8') as file:
        data = load(file)
    data[field] = content.encode('utf-8').decode('utf-8')
    file_fill(user_id, data=data)


@dp.message_handler(state=TestStates.TEST_STATE_0)
async def state0(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    change_user_file(message.from_user.id, 'name', message.text)
    await message.reply('Спасибо!', reply=False)
    await message.reply('Напиши свое хобби!', reply=False)
    await state.set_state(TestStates.all()[1])

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def state1(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    change_user_file(message.from_user.id, 'hobby', message.text)
    await message.reply('Спасибо!', reply=False)
    await message.reply('Напиши свой возраст (полных лет)!', reply=False)
    await state.set_state(TestStates.all()[2])

@dp.message_handler(state=TestStates.TEST_STATE_2)
async def state2(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    age = message.text
    if age.isdigit() and 2 <= int(age) <= 150:
        change_user_file(message.from_user.id, 'age', age)
        await message.reply('Спасибо!', reply=False)
        await message.reply('Опрос окончен', reply=False)
        return await state.reset_state()
    else:
        await message.reply('Напиши свой возраст (полных лет)! от 2 до 150 лет!', reply=False)


# echo
@dp.message_handler()
async def echo(message: types.Message):
    msg_text = message.text

    if msg_text == 'Hello':
        await bot.send_message(message.from_user.id, "Bongour")
    else:
        await bot.send_message(message.from_user.id, message.text)
    # print(message)

# stickers, photos and other
@dp.message_handler(content_types=ContentType.ANY)
async def any_format(message: types.Message):
    msgtext = text(emojize("Я не знаю, что с этим делать :astonished:"),
                    italic('Я просто напомню, что есть'),
                    code('команда'), "/help"
                                )
    await bot.send_message(message.from_user.id, msgtext, parse_mode=ParseMode.MARKDOWN)
#
if __name__ == '__main__':
    print('bot is waiting :)')
    executor.start_polling(dp)


