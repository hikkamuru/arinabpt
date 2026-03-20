import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
HER_NAME = os.getenv("HER_NAME", "Арина")
HIS_NAME = os.getenv("HIS_NAME", "Максим")
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "")
