from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove

from bot_db import *
from buttons import *


TOKEN = '5846191784:AAHRbeVwS5SfmfzgSI0gFDNbOCrushXr6S8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 1908084892


class FSMAdmin(StatesGroup):
    choice = State()


def auth(func):
    """

    Проверка доступа по id

    :param func:
    :return:
    """
    async def wrapper(message, state):
        if message.from_user.id != admin_id:
            return await message.answer('Отказано в доступе', reply_markup=ReplyKeyboardRemove())
        return await func(message, state)

    return wrapper


@auth
async def start(message: types.Message, state: FSMContext):
    await message.answer('Выберите действия', reply_markup=choice_kb)
    await state.set_state(FSMAdmin.choice.state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
