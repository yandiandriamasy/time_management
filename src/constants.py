from dotenv import load_dotenv
from src.paths import ENV_PATH
import os

load_dotenv(ENV_PATH, override=True)
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("TABLE_ID")
PRIM_API_KEY = os.getenv("PRIM_TOKEN")

## PRIM CONSTANTS
REFERENCE_RUEIL_RER_A = "STIF%3AStopArea%3ASP%3A58875%3A"