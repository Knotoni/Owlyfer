from aiogram.types import *
from aiogram.dispatcher.filters import *
from aiogram.dispatcher.filters.state import *
from aiogram.utils.callback_data import *
from aiogram.dispatcher.storage import *
from aiogram.types.inline_keyboard import *
from utils.loader import *
from utils.db_reader import *
from utils.keyboards import *
from emoji import *

@dp.message_handler(commands=['start'])
async def hello_message(message: Message):
    user_tg_id = message.from_user.id
    if users.find(user_tg_id) == False:
        users.add(user_tg_id)
    channel = await bot.get_chat(CHANNEL)
    await message.answer(f"Добро пожаловать в предложку канала {channel.full_name}\n" + \
        "Советуем прочитать раздел <b>'Помощь'</b>", reply_markup=kbrd_user_main)

@dp.message_handler(text = btn_help.text)
async def help_message(message: Message):
    msg_text = "Добро пожаловать в бот-предложку\n" + \
        "Чтобы предложить пост нажмите кнопку 'Предложить пост', после чего отправьте сформированный пост" + \
        "После отправки он будет добавлен в предложенные посты, после чего администраторы его примут, либо отклонят" + \
        "После принятия (отклонения) вам будет прислано уведомление, какой пост был принят (отклонен)"
    await message.answer(msg_text)

@dp.message_handler(text = btn_about_bot.text)
async def about_message(message: Message):
    msg_text = "Бот написан @Knotoni\n"
    await message.answer(msg_text)