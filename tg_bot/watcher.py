import asyncio
import json
from pathlib import Path
from aiogram import Bot
from .config import REPORTS_PATH, ALLOWED_USERS


class ReportsWatcher:
    def __init__(self, bot: Bot, interval: int = 10):
        self.bot = bot
        self.interval = interval
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.sent_file = self.data_dir / "sent.json"
        self.sent: set[str] = self._load_sent()

    def _load_sent(self) -> set[str]:
        if self.sent_file.exists():
            try:
                with open(self.sent_file, "r", encoding="utf-8") as f:
                    return set(json.load(f))
            except Exception:
                return set()
        return set()

    def _save_sent(self):
        with open(self.sent_file, "w", encoding="utf-8") as f:
            json.dump(list(self.sent), f, ensure_ascii=False, indent=2)

    def scan_reports(self) -> list[tuple[str, str, Path]]:
        new_files = []
        for testset_dir in REPORTS_PATH.iterdir():
            if not testset_dir.is_dir():
                continue
            for date_dir in testset_dir.iterdir():
                if not date_dir.is_dir():
                    continue
                for file in date_dir.glob("*.html"):
                    key = str(file.resolve())
                    if key not in self.sent:
                        self.sent.add(key)
                        new_files.append((testset_dir.name, date_dir.name, file))
        if new_files:
            self._save_sent()
        return new_files

    async def run(self):
        while True:
            new_reports = self.scan_reports()
            for testset, date, file in new_reports:
                caption = f"{testset} {date}"
                for user_id in ALLOWED_USERS:
                    await self.bot.send_document(user_id, file.open("rb"), caption=caption)
            await asyncio.sleep(self.interval)
