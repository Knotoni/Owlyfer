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

class adding_admin(StatesGroup):
    get_tg_id = State()
    get_nick = State()

class deleting_admin(StatesGroup):
    get_tg_id = State()

class banning_user(StatesGroup):
    get_tg_id = State()

class unbanning_user(StatesGroup):
    get_tg_id = State()

@dp.message_handler(commands = ["admin"])
async def show_admin_panel(message: Message):
    if admins.check(message.from_user.id):
        await message.answer("Добро пожаловать в панель администратора", reply_markup=kbrd_admin_main)

@dp.message_handler(text = btn_admin_list.text)
async def show_admin_list(message: Message):
    if admins.check(message.from_user.id):
        admin_list = admins.get_all()
        msg_text = "<b>Список админов:</b>\n\n"
        for i in admin_list:
            msg_text += f"<b>{i[2]}</b> ({i[1]})\n"
        await message.answer(msg_text)

@dp.message_handler(text = btn_ban_user.text)
async def ban_user(message: Message):
    if admins.check(message.from_user.id):
        await message.answer("Введите Telegram ID пользователя, которого хотите забанить", reply_markup = kbrd_stop_action)
        await banning_user.get_tg_id.set()

@dp.message_handler(state = banning_user.get_tg_id)
async def ban_user_complete(message: Message, state: FSMContext):
    try:
        user = await bot.get_chat(message.text)
        users.ban(user.id)
        await message.answer(f"Пользователь {user.full_name} забанен", reply_markup = kbrd_admin_main)
        await state.finish()
    except:
        await message.answer("Ошибка! Проверьте правильность вводимого ID")

@dp.message_handler(state = banning_user.get_tg_id, text = btn_stop.text)
async def ban_user_break(message: Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup = kbrd_admin_main)
    await state.finish()

@dp.message_handler(text = btn_unban_user.text)
async def unban_user(message: Message):
    if admins.check(message.from_user.id):
        await message.answer("Введите Telegram ID пользователя, которого хотите разбанить", reply_markup = kbrd_stop_action)
        await unbanning_user.get_tg_id.set()

@dp.message_handler(state = unbanning_user.get_tg_id)
async def unban_user_complete(message: Message, state: FSMContext):
    try:
        user = await bot.get_chat(message.text)
        users.unban(user.id)
        await message.answer(f"Пользователь {user.full_name} разбанен", reply_markup = kbrd_admin_main)
        await state.finish()
    except:
        await message.answer("Ошибка! Проверьте правильность вводимого ID")

@dp.message_handler(state = unbanning_user.get_tg_id, text = btn_stop.text)
async def unban_user_break(message: Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup = kbrd_admin_main)
    await state.finish()

@dp.message_handler(text = btn_add_admin.text)
async def add_admin(message: Message):
    if admins.check(message.from_user.id):
        await message.answer("Введите Telegram ID администратора, которого хотите добавить " + \
            "(добавляемый администратор должен запустить бота хотя бы один раз)", reply_markup = kbrd_stop_action)
        await adding_admin.get_tg_id.set()

@dp.message_handler(state = adding_admin.all_states, text = btn_stop.text)
async def add_admin_break(message: Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup = kbrd_admin_main)
    await state.finish()

@dp.message_handler(state = adding_admin.get_tg_id, content_types=ContentType.TEXT)
async def add_admin_get_id(message: Message, state: FSMContext):
    try:
        user = await bot.get_chat(message.text)
        await state.update_data(tg_id = user.id)
        await message.answer("Введите ник администратора")
        await adding_admin.next()
    except:
        await message.answer("Ошибка! Проверьте правильность вводимого ID")

@dp.message_handler(state = adding_admin.get_nick, content_types = ContentType.TEXT)
async def add_admin_done(message: Message, state: FSMContext):
    async with state.proxy() as data:
        tg_id = data["tg_id"]
    admins.add(tg_id, message.text)
    user = await bot.get_chat(tg_id)
    await message.answer(f"Администратор {user.full_name} добавлен", reply_markup = kbrd_admin_main)
    await state.finish()

@dp.message_handler(text = btn_del_admin.text)
async def del_admin(message: Message):
    if admins.check(message.from_user.id):
        await message.answer("Введите Telegram ID администратора, которого хотите удалить", reply_markup = kbrd_stop_action)
        await deleting_admin.get_tg_id.set()

@dp.message_handler(state = deleting_admin.get_tg_id)
async def del_admin_complete(message: Message, state: FSMContext):
    try:
        user = await bot.get_chat(message.text)
        admins.delete(user.id)
        await message.answer(f"Администратор {user.full_name} удален", reply_markup = kbrd_admin_main)
        await state.finish()
    except:
        await message.answer("Ошибка! Проверьте правильность вводимого ID")

@dp.message_handler(state = deleting_admin.get_tg_id, text = btn_stop.text)
async def del_admin_break(message: Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup = kbrd_admin_main)
    await state.finish()