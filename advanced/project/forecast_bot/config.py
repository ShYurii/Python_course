import os
from dataclasses import dataclass
from dotenv import load_dotenv # ??

load_dotenv()

@dataclass
class Config:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    OPENWEATHER_TOKEN: str = os.getenv("OPENWEATHER_TOKEN", "")
    DB_PATH: str = os.getenv("DB_PATH", "forecast_bot.db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

cfg = Config()
