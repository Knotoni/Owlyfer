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

post_actions = CallbackData("post_actions", "action", "post_id")

async def create_media_group(post_id: int, type: str):
    media = []
    post = posts.get(post_id)
    files_list = files.get_post(post_id)
    user_tg_id = users.get_tg_id(post[1])
    user_name = await bot.get_chat(user_tg_id)
    user_name = user_name.full_name
    if type == "admin":
        if post[2] != None:
            caption = post[2] + f"\nПредложил - {user_name} ({user_tg_id})"
        else:
            caption = f"Предложил - {user_name} ({user_tg_id})"
    else:
        if post[2] != None:
            caption = post[2] + f"\nПредложил(а) - {user_name}"
        else:
            caption = f"Предложил(а) - {user_name}"
    files_list.reverse()
    for i in files_list:
        if i[3] == "img":
            if media.__len__() == 0: media += [InputMediaPhoto(i[2], caption = caption)]
            else: media += [InputMediaPhoto(i[2])]
        elif i[3] == "video":
            if media.__len__() == 0: media += [InputMediaVideo(i[2], caption = caption)]
            else: media += [InputMediaVideo(i[2])]
        elif i[3] == "audio":
            if media.__len__() == 0: media += [InputMediaAudio(i[2], caption = caption)]
            else: media += [InputMediaAudio(i[2])]
        elif i[3] == "doc":
            if media.__len__() == 0: media += [InputMediaDocument(i[2], caption = caption)]
            else: media += [InputMediaDocument(i[2])]
    media.reverse()
    return media

async def send_post_to_admins(post_id: int):
    admin_list = admins.get_all()
    for i in admin_list:
        btn_accept_post = InlineKeyboardButton("Принять", callback_data=post_actions.new(action = "accept", post_id = post_id))
        btn_decline_post = InlineKeyboardButton("Отклонить", callback_data=post_actions.new(action = "decline", post_id = post_id))
        kbrd_post_action = InlineKeyboardMarkup(row_width=2).add(btn_accept_post, btn_decline_post)
        post_files = files.get_post(post_id)
        post = posts.get(post_id)
        admin_id = admins.get(i[1])
        if post_files != None:
            media = await create_media_group(post_id, "admin")
            await bot.send_media_group(i[1], media)
            msg = await bot.send_message(i[1], "Что сделать с постом?", reply_markup=kbrd_post_action)
            post_state.add(post_id, msg.message_id, admin_id[0])
        else:
            user_tg_id = users.get_tg_id(post[1])
            user_name = await bot.get_chat(user_tg_id)
            user_name = user_name.full_name
            await bot.send_message(i[0], post[2] + f"\nПредложил - {user_name} ({user_tg_id})")
            msg = await bot.send_message(i[0], "Что сделать с постом?", reply_markup=kbrd_post_action)
            post_state.add(post_id, msg.message_id, admin_id[0])

@dp.callback_query_handler(post_actions.filter(action = "accept"))
async def accept_post(query: CallbackQuery, callback_data: dict):
    if admins.check(query.from_user.id):
        post_id = callback_data.get("post_id")
        post_files = files.get_post(post_id)
        post = posts.get(post_id)
        admin_list = admins.get_all()
        accept_admin = (admins.get(query.from_user.id))[2]
        user_tg_id = users.get_tg_id(post[1])
        user_name = await bot.get_chat(user_tg_id)
        user_name = user_name.full_name
        if post_files != None:
            media =  await create_media_group(post_id, "user")
            await bot.send_media_group(CHANNEL, media)
        else:
            
            await bot.send_message(CHANNEL, post[2] + f"\nПредложил - {user_name}")
        for i in admin_list:
            msg_id = post_state.get(post_id, i[0])
            await bot.edit_message_text(f"Пост принял(а) {accept_admin}", i[1], msg_id)
        await bot.send_message(user_tg_id, f"Вас пост приняли!\nID поста - {post_id}")
        post_state.delete(post_id)
        posts.delete(post_id)
        files.delete_post(post_id)
                
@dp.callback_query_handler(post_actions.filter(action = "decline"))
async def decline_post(query: CallbackQuery, callback_data: dict):
    if admins.check(query.from_user.id):
        post_id = callback_data.get("post_id")
        post = posts.get(post_id)
        admin_list = admins.get_all()
        accept_admin = (admins.get(query.from_user.id))[2]
        user_tg_id = users.get_tg_id(post[1])
        user_name = await bot.get_chat(user_tg_id)
        user_name = user_name.full_name
        for i in admin_list:
            msg_id = post_state.get(post_id, i[0])
            await bot.edit_message_text(f"Пост отклонил(а) {accept_admin}", i[1], msg_id)
        await bot.send_message(user_tg_id, f"Вас пост отклонили!\nID поста - {post_id}")
        post_state.delete(post_id)
        posts.delete(post_id)
        files.delete_post(post_id)