from aiogram.types.reply_keyboard import *
from aiogram.types.inline_keyboard import *
from emoji import *

#Базовые клавиатуры
btn_stop = KeyboardButton(emojize(":stop_sign: Отмена"))
btn_next = KeyboardButton(emojize(":play_button: Далее"))

kbrd_stop_action = ReplyKeyboardMarkup(resize_keyboard=True)
kbrd_stop_action.add(btn_stop)

kbrd_stop_and_next = ReplyKeyboardMarkup(resize_keyboard=True)
kbrd_stop_and_next.add(btn_stop, btn_next)

#Клавиатуры для юзера
btn_help = KeyboardButton(emojize(":face_with_monocle: Помощь"))
btn_about_bot = KeyboardButton(emojize(":owl: О боте"))
btn_suggest_post = KeyboardButton(emojize(":envelope: Предложить пост"))

kbrd_user_main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kbrd_user_main.add(btn_suggest_post)
kbrd_user_main.add(btn_help, btn_about_bot)

#Клавиатуры для админа
btn_ban_user = KeyboardButton(emojize(":kitchen_knife: Забанить пользователя"))
btn_unban_user = KeyboardButton(emojize(":recycling_symbol: Разбанить пользователя"))
btn_add_admin = KeyboardButton(emojize(":key: Добавить админа"))
btn_del_admin = KeyboardButton(emojize(":locked: Удалить админа"))
btn_admin_list = KeyboardButton(emojize(":card_file_box: Список админов"))

kbrd_admin_main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
kbrd_admin_main.add(btn_ban_user, btn_unban_user, btn_add_admin, btn_del_admin, btn_admin_list)