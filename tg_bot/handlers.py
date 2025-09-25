from aiogram import Router, types
from aiogram.filters import Command
from bot_config import ALLOWED_USERS

router = Router()

SENT_FILE = Path(__file__).parent / "data" / "sent.json"

def load_sent() -> dict[str, dict]:
    """Загружает sent.json {путь: {id,testset,date}}."""
    if SENT_FILE.exists():
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    return
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer(
        "Бот следит за новыми отчётами в /reports.\n"
        "Будет присылать ссылки сюда."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    return
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer("/start — запустить\n/help — подсказка")


@router.message()
async def handle_report_request(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS:
        return

    user_text = message.text.strip()
    sent = load_sent()  # загружаем словарь {путь: id}

    for path, rep_id in sent.items():
        if rep_id == user_text:
            file_path = Path(path)
            if file_path.exists():
                doc = FSInputFile(file_path)
                await message.answer_document(doc, caption=f"Отчёт {rep_id}")
                return

    await message.answer("Отчёт с таким ID не найден.")
