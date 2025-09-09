import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPORTS_PATH = Path("../reports")

# список ID через запятую: "12345,67890"
ALLOWED_USERS = {int(x) for x in os.getenv("ALLOWED_USERS", "").split(",") if x}
