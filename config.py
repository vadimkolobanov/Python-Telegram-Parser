import os

from dotenv import load_dotenv

load_dotenv()

# Получение значения DSN
DB_NAME = os.getenv("DATABASE_URL")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USERNAME = os.getenv("USERNAME")
