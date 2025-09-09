import os
from pathlib import Path

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPORTS_PATH = Path("../reports").resolve()
