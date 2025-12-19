import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import cfg
from db.database import Database

from handlers.commands import router as commands_router
from handlers.location import router as location_router
from handlers.weather import router as weather_router
from handlers.city import router as city_router

logging.basicConfig(level=cfg.LOG_LEVEL)
logger = logging.getLogger(__name__)

bot = Bot(token=cfg.TELEGRAM_TOKEN)
dp = Dispatcher()
db = Database(cfg.DB_PATH)


async def main():
    await db.connect()

    # Inject database into dispatcher
    dp["db"] = db

    # Include all routers
    dp.include_router(commands_router)
    dp.include_router(location_router)
    dp.include_router(weather_router)
    dp.include_router(city_router)

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
