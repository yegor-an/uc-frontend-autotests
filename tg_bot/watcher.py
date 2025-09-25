import asyncio
import json
import random
import string
from pathlib import Path
from aiogram import Bot
from bot_config import REPORTS_PATH, ALLOWED_USERS
from bs4 import BeautifulSoup  # pip install beautifulsoup4


class ReportsWatcher:
    def __init__(self, bot: Bot, interval: int = 10):
        self.bot = bot
        self.interval = interval
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.sent_file = self.data_dir / "sent.json"
        self.sent: dict[str, dict] = self._load_sent()
        print(f"[Watcher] Запущен. Файл sent.json: {self.sent_file}")

    def _load_sent(self) -> dict[str, dict]:
        if self.sent_file.exists():
            try:
                with open(self.sent_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        return loaded
            except Exception as e:
                print(f"[Watcher] Ошибка чтения sent.json: {e}")
        print("[Watcher] sent.json не найден, начинаем с пустого списка.")
        return {}

    def _save_sent(self):
        try:
            with open(self.sent_file, "w", encoding="utf-8") as f:
                json.dump(self.sent, f, ensure_ascii=False, indent=2)
            print(f"[Watcher] Сохранили {len(self.sent)} отправленных отчётов.")
        except Exception as e:
            print(f"[Watcher] Ошибка записи sent.json: {e}")

    @staticmethod
    def _generate_id(length: int = 6) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def scan_reports(self) -> list[tuple[str, str, Path, str]]:
        new_files = []
        #print(f"[Watcher] Сканирую папку {REPORTS_PATH}...")
        for testset_dir in REPORTS_PATH.iterdir():
            if not testset_dir.is_dir():
                continue
            for date_dir in testset_dir.iterdir():
                if not date_dir.is_dir():
                    continue
                for file in date_dir.glob("*.html"):
                    key = str(file.resolve())
                    if key not in self.sent:
                        report_id = self._generate_id()
                        self.sent[key] = {
                            "id": report_id,
                            "testset": testset_dir.name,
                            "date": date_dir.name,
                        }
                        new_files.append((testset_dir.name, date_dir.name, file, report_id))
                        print(f"[Watcher] Найден новый отчёт: {file}")
        if new_files:
            self._save_sent()
        return new_files

    @staticmethod
    def parse_report(file: Path) -> dict[str, int]:
        """Парсит HTML и вытаскивает числа из блока .filters по классам span."""
        try:
            soup = BeautifulSoup(file.read_text(encoding="utf-8"), "html.parser")
            spans = soup.select("div.filters span")
            stats = {}
            for span in spans:
                classes = span.get("class", [])
                if not classes:
                    continue
                cls = classes[0]  # например 'failed', 'passed', 'skipped'
                text = span.get_text(strip=True)  # '0 Failed,' или '16 Passed,'
                num = text.split()[0]  # '0' или '16'
                try:
                    stats[cls] = int(num)
                except ValueError:
                    stats[cls] = 0
            return stats
        except Exception as e:
            print(f"[Watcher] Ошибка парсинга {file}: {e}")
            return {}

    @staticmethod
    def format_summary(stats: dict[str, int], report_id: str) -> str:
        """Формирует текстовую сводку по заданному порядку."""
        passed = stats.get("passed", 0)
        failed = stats.get("failed", 0)
        errors = stats.get("error", 0)
        skipped = stats.get("skipped", 0)
        expected_failures = stats.get("xfailed", 0)
        unexpected_passes = stats.get("xpassed", 0)
        reruns = stats.get("rerun", 0)

        return (
            f"✅ Passed: {passed}\n"
            f"❌ Failed: {failed}\n"
            f"❌ Errors: {errors}\n"
            f"⚠️ Skipped: {skipped}\n"
            f"🟡 Expected failures: {expected_failures}\n"
            f"🔵 Unexpected passes: {unexpected_passes}\n"
            f"🔁 Reruns: {reruns}\n\n"
            f"<code>{report_id}</code>"
        )

    async def run(self):
        print("[Watcher] Цикл запущен, ожидаем новые отчёты.")
        while True:
            new_reports = self.scan_reports()
            for testset, date, file, report_id in new_reports:
                stats = self.parse_report(file)
                summary = self.format_summary(stats, report_id)
                # сообщение: testset + date + сводка
                text_message = f"{testset} {date}\n\n{summary}"
                for user_id in ALLOWED_USERS:
                    try:
                        await self.bot.send_message(user_id, text_message, parse_mode="HTML")
                        print(f"[Watcher] Сводка отчёта {file} ({testset} {date}) отправлена пользователю {user_id}")
                    except Exception as e:
                        print(f"[Watcher] Ошибка отправки сводки {file} пользователю {user_id}: {e}")
            await asyncio.sleep(self.interval)
