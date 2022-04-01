from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser

#Загружаем токен бота и telegram_id главного админа
config = configparser.ConfigParser()
config.read('data/bot_info.ini')
BOT_TOKEN = config.get('telegram', 'bot_token')
ADMIN_TG_ID = config.get('telegram', 'admin_id')
CHANNEL = config.get('telegram', 'channel_id')

#Инициализируем бота, диспатчер и MemoryStorage
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)