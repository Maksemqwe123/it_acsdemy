from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('добавить аккаунт'),
    KeyboardButton('Удалить аккаунт')
).row(
    KeyboardButton('Удалить все аккаунты')
).row(
    KeyboardButton('Получить информацию')
)

cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Отмена действий')
)

delete_choice_buttons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Да')
).add(
    KeyboardButton('Нет')
)
