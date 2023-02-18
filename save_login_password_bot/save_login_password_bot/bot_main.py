from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove

from bot_db import *
from buttons import *
from save_login_password_bot.middlewares import AccessMiddleware


TOKEN = '5846191784:AAHRbeVwS5SfmfzgSI0gFDNbOCrushXr6S8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 1908084892

dp.middleware.setup(AccessMiddleware(admin_id))

database = DataBase('user_bot')


class FSMAdmin(StatesGroup):
    choice = State()
    get_login = State()
    delete_account = State()
    delete_all_accounts = State()
    get_password = State()


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


async def start(message: types.Message, state: FSMContext):
    await message.answer('Выберите действия', reply_markup=choice_kb)
    await state.set_state(FSMAdmin.choice.state)


async def choice(message: types.Message, state: FSMContext):
    if message.text.lower() == 'добавить аккаунт':
        await message.answer('Введите логин', reply_markup=cancel_kb)
        await state.set_state(FSMAdmin.get_login.state)

    elif message.text.lower() == 'удалить аккаунт':
        await message.answer('Введите логин для удаление', reply_markup=cancel_kb)
        await state.set_state(FSMAdmin.delete_account.state)

    elif message.text.lower() == 'удалить все аккаунты':
        await message.answer('Вы дествительно хотите удалить все аккаунты', reply_markup=delete_choice_buttons)
        await state.set_state(FSMAdmin.delete_all_accounts.state)

    elif message.text.lower() == 'получить информацию':
        all_info = database.read_info()
        for account in all_info:
            await message.answer(account)


async def delete_all_accounts(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        response = database.delete_all_accounts()
        await message.answer(response, reply_markup=choice_kb)
        await state.set_state(FSMAdmin.choice.state)

    elif message.text.lower() == 'нет':
        await message.answer('Действие отменено', reply_markup=choice_kb)
        await state.set_state(FSMAdmin.choice.state)


async def delete_account(message: types.Message, state: FSMContext):
    response = database.delete_account(message.text)
    await message.answer(response, reply_markup=choice_kb)
    await state.set_state(FSMAdmin.choice.state)


async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer('Введите пароль', reply_markup=cancel_kb)
    await state.set_state(FSMAdmin.get_password.state)


async def get_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data.get('login')
    password = message.text

    response = database.add_account(login, password)
    await message.answer(response, reply_markup=choice_kb)
    await state.set_state(FSMAdmin.choice.state)


async def cancel(message: types.Message, state: FSMContext):
    await message.reply('Ввод отменен', reply_markup=choice_kb)
    await state.set_state(FSMAdmin.choice.state)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=['отмена', 'cancel'], state='*')
    dp.register_message_handler(cancel, Text(equals='отмена действий', ignore_case=True), state='*')

    dp.register_message_handler(start, commands='start')

    dp.register_message_handler(choice, state=FSMAdmin.choice)

    dp.register_message_handler(delete_all_accounts, state=FSMAdmin.delete_all_accounts)

    dp.register_message_handler(delete_account, state=FSMAdmin.delete_account)

    dp.register_message_handler(get_login, state=FSMAdmin.get_login)

    dp.register_message_handler(get_password, state=FSMAdmin.get_password)


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
