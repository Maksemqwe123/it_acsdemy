from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bth_profile = KeyboardButton('Профиль')
bth_sub = KeyboardButton('Подписка')
bth_delete = KeyboardButton('Удалить профиль')


main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(bth_profile, bth_sub)
main_menu.add(bth_delete)
