import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove

from database import DataBase
from keybords import *

TOKEN = '5846191784:AAHRbeVwS5SfmfzgSI0gFDNbOCrushXr6S8'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = DataBase('users.db')


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not db.user_exist(message.from_user.id):
        db.add_user(message.from_user.id)
        await message.answer("Укажите свой ник", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Вы уже зарегистрированы', reply_markup=main_menu)


@dp.message_handler()
async def add_user(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Профиль':
            username = db.get_username(user_id=message.from_user.id)
            await message.answer(f'Ваш ник: {username}')

        elif message.text == 'Удалить профиль':
            try:
                db.delete_user(user_id=message.from_user.id)
            except:
                await message.answer('Произошла ошибка')

        elif message.text == 'Подписка':
            if db.get_signup(user_id=message.from_user.id) == 'done':
                await message.answer('вы подписаны')

        else:
            if db.get_signup(user_id=message.from_user.id) == 'setusername':
                if len(message.text) > 15:
                    await message.answer('Ник не должен превышать 15 символов')
                elif '@' in message.text or '/' in message.text:
                    await message.answer('Вы ввели запрещенный символ')
                else:
                    db.set_username(user_id=message.from_user.id, username=message.text)
                    db.set_signup(user_id=message.from_user.id, signup='done')
                    await message.answer('Регистрация прошла успешно', reply_markup=main_menu)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
