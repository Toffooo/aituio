from decouple import config
from pathlib import Path


ABS_PATH = Path().resolve()

TELEGRAM_BOT_API_TOKEN = config("TELEGRAM_BOT_API_TOKEN", cast=str)
DATABASE_URL = config("DATABASE_URL", cast=str)
ADMIN_IDS = config("ADMIN_IDS", cast=str).split(",")
USE_REDIS = config("USE_REDIS", cast=str)


class CeleryConfigDocker:
    broker_url = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "UTC"
