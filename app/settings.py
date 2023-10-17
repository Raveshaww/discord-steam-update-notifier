import os
import pathlib
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# DB_URL = os.getenv("sqlalchemy.url")

# ALEMBIC_URL = os.getenv(alembic.url")

DB_USER = os.getenv("POSTGRES_USERNAME")

DB_PASS = os.getenv("POSTGRES_PASSWORD")

DB_HOST = os.getenv("POSTGRES_HOST")

DB_NAME = os.getenv("POSTGRES_DB")

BASE_DIR = pathlib.Path(__file__).parent

MODELS_DIR = BASE_DIR / "models"
