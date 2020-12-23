from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.utils.emoji import emojize
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode

from config import TOKEN

####

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import TestStates

from json import dump, load


# Создание бота по токену
bot = Bot(token=TOKEN)
# dispatcher
# dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
###############


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.reply('Привет! Напиши мне что-нибудь!')


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply('Слушаюсь и повинуюсь!')
    await bot.send_message(message.from_user.id, """
Доступные команды:
/start,
/help,
/photo    
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

def change_user_file(user_id, field, content):
    with open(f'user_data/{user_id}.json', 'r', encoding='utf-8') as file:
        data = load(file)
    data[field] = content
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


