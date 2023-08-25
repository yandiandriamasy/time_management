from dotenv import load_dotenv
from src.paths import ENV_PATH
import os

load_dotenv(ENV_PATH, override=True)
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("TABLE_ID")
