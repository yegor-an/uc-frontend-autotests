import asyncio
import json
from pathlib import Path
from aiogram import Bot
from aiogram.types import FSInputFile
from bot_config import REPORTS_PATH, ALLOWED_USERS


class ReportsWatcher:
    def __init__(self, bot: Bot, interval: int = 10):
        self.bot = bot
        self.interval = interval
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.sent_file = self.data_dir / "sent.json"
        self.sent: set[str] = self._load_sent()
        print(f"[Watcher] Запущен. Файл sent.json: {self.sent_file}")

    def _load_sent(self) -> set[str]:
        if self.sent_file.exists():
            try:
                with open(self.sent_file, "r", encoding="utf-8") as f:
                    loaded = set(json.load(f))
                    print(f"[Watcher] Загружено {len(loaded)} уже отправленных отчётов.")
                    return loaded
            except Exception as e:
                print(f"[Watcher] Ошибка чтения sent.json: {e}")
                return set()
        print("[Watcher] sent.json не найден, начинаем с пустого списка.")
        return set()

    def _save_sent(self):
        try:
            with open(self.sent_file, "w", encoding="utf-8") as f:
                json.dump(list(self.sent), f, ensure_ascii=False, indent=2)
            print(f"[Watcher] Сохранили {len(self.sent)} отправленных отчётов.")
        except Exception as e:
            print(f"[Watcher] Ошибка записи sent.json: {e}")

    def scan_reports(self) -> list[tuple[str, str, Path]]:
        new_files = []
        print(f"[Watcher] Сканирую папку {REPORTS_PATH}...")
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
                        print(f"[Watcher] Найден новый отчёт: {file}")
        if new_files:
            self._save_sent()
        return new_files

    async def run(self):
        print("[Watcher] Цикл запущен, ожидаем новые отчёты.")
        while True:
            new_reports = self.scan_reports()
            for testset, date, file in new_reports:
                caption = f"{testset} {date}"
                for user_id in ALLOWED_USERS:
                    try:
                        doc = FSInputFile(file)  # <=== оборачиваем путь в FSInputFile
                        await self.bot.send_document(user_id, doc, caption=caption)
                        print(f"[Watcher] Отправлен {file} пользователю {user_id}")
                    except Exception as e:
                        print(f"[Watcher] Ошибка отправки {file} пользователю {user_id}: {e}")
            await asyncio.sleep(self.interval)
