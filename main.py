import logging, handlers
from utils.loader import dp
from aiogram import executor
from utils.db_reader import check_db

if __name__ == "__main__":
    check_db()
    executor.start_polling(dp, skip_updates=True)

logging.basicConfig(level=logging.INFO)