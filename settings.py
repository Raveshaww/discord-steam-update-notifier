import os
import pathlib
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

DB_URL = os.getenv("sqlalchemy.url")

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"

MODELS_DIR = BASE_DIR / "models"

TASKS_DIR = BASE_DIR / "tasks"
