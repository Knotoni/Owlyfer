from aiogram.types import *
from aiogram.dispatcher.filters import *
from aiogram.dispatcher.filters.state import *
from aiogram.utils.callback_data import *
from aiogram.dispatcher.storage import *
from aiogram.types.inline_keyboard import *
from handlers.admins.posting_module import send_post_to_admins
from utils.loader import *
from utils.db_reader import *
from utils.keyboards import *
from emoji import *

class suggesting_post (StatesGroup):
    get_post = State()
    inform_user = State()


@dp.message_handler(text = btn_suggest_post.text)
async def suggest_post(message: Message):
    if users.chech_ban(message.from_user.id):
        await message.answer("Отправьте пост, который вы хотите предложить, после чего нажмите 'Далее'", reply_markup=kbrd_stop_and_next)
        await suggesting_post.get_post.set()
    else:
        await message.answer("Извините, но вы забанены в этом боте навсегда")

@dp.message_handler(text = btn_stop.text, state = suggesting_post.all_states)
async def suggest_post_stop(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
            files.delete_post(post_id)
            posts.delete(post_id)
            await state.finish()
        except:
            await state.finish()
    await message.answer("Отмена создания поста", reply_markup=kbrd_user_main)

@dp.message_handler(state = suggesting_post.get_post, content_types = ContentTypes.PHOTO)
async def suggest_post_get_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
        except:
            if bool(message.caption):
                post_text = message.caption
                post_id = posts.add(message.from_user.id, post_text)
                await state.update_data(post_id = post_id)
            else:
                post_id = posts.add(message.from_user.id, None)
                await state.update_data(post_id = post_id)
    if bool(files.get_post(post_id)):
        if len(files.get_post(post_id)) >= 10:
            await suggesting_post.next()
        else:
            files.add(post_id, message.photo[0].file_id, "img")
    else:
        files.add(post_id, message.photo[0].file_id, "img")

@dp.message_handler(state = suggesting_post.get_post, content_types = ContentTypes.AUDIO)
async def suggest_post_get_audio(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
        except:
            if bool(message.caption):
                post_text = message.caption
                post_id = posts.add(message.from_user.id, post_text)
                await state.update_data(post_id = post_id)
            else:
                post_id = posts.add(message.from_user.id, None)
                await state.update_data(post_id = post_id)
    if bool(files.get_post(post_id)):
        if len(files.get_post(post_id)) >= 10:
            await suggesting_post.next()
        else:
            files.add(post_id, message.audio.file_id, "audio")
    else:
        files.add(post_id, message.audio.file_id, "audio")

@dp.message_handler(state = suggesting_post.get_post, content_types = ContentTypes.VIDEO)
async def suggest_post_get_video(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
        except:
            if bool(message.caption):
                post_text = message.caption
                post_id = posts.add(message.from_user.id, post_text)
                await state.update_data(post_id = post_id)
            else:
                post_id = posts.add(message.from_user.id, None)
                await state.update_data(post_id = post_id)
    if bool(files.get_post(post_id)):
        if len(files.get_post(post_id)) >= 10:
            await suggesting_post.next()
        else:
            files.add(post_id, message.video.file_id, "video")
    else:
        files.add(post_id, message.video.file_id, "video")

@dp.message_handler(state = suggesting_post.get_post, content_types = ContentTypes.DOCUMENT)
async def suggest_post_get_doc(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
        except:
            if bool(message.caption):
                post_text = message.caption
                post_id = posts.add(message.from_user.id, post_text)
                await state.update_data(post_id = post_id)
            else:
                post_id = posts.add(message.from_user.id, None)
                await state.update_data(post_id = post_id)
    if bool(files.get_post(post_id)):
        if len(files.get_post(post_id)) >= 10:
            await suggesting_post.next()
        else:
            files.add(post_id, message.document.file_id, "doc")
    else:
        files.add(post_id, message.document.file_id, "doc")

@dp.message_handler(state = suggesting_post.get_post, content_types = ContentTypes.TEXT)
async def suggest_post_get_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            post_id = int(data["post_id"])
            await message.answer("Вы действительно хотите отправить этот пост?")
        except:
            post_text = message.text
            post_id = posts.add(message.from_user.id, post_text)
            await state.update_data(post_id = post_id)
    await suggesting_post.next()

@dp.message_handler(state = suggesting_post.get_post, text = btn_next.text)
async def suggest_post_continue(message: Message, state: FSMContext):
    await message.answer("Вы действительно хотите отправить этот пост?")
    await suggesting_post.next()

@dp.message_handler(state = suggesting_post.inform_user, text = btn_next.text)
async def suggest_post_done(message: Message,state: FSMContext):
    async with state.proxy() as data:
        post_id = int(data["post_id"])
    await send_post_to_admins(post_id)
    await message.answer(f"Ваш пост поступил, ожидайте решения админов о публикации\nID поста - {post_id}", reply_markup=kbrd_user_main)
    await state.finish()