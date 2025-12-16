# bot.py
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from config import cfg
from db.database import Database
# from handlers.commands import register_commands_handlers
from handlers.commands import router as commands_router


logging.basicConfig(level=cfg.LOG_LEVEL)
logger = logging.getLogger(__name__)

bot = Bot(token=cfg.TELEGRAM_TOKEN)
dp = Dispatcher()
db = Database(cfg.DB_PATH)

# подключаем middlewares / filters / routers здесь, например:
# dp.message.middleware(LogMiddleware())
# dp.include_router(user_router) etc.

async def main():
    await db.connect()
    # регистрация хендлеров
    # register_commands_handlers(dp, db)   # пример: передаем dp и db в регистрацию
    dp.include_router(commands_router)
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
