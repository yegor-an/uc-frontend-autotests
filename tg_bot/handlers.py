from aiogram import Router, types
from aiogram.filters import Command
from bot_config import ALLOWED_USERS

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer(
        "Бот следит за новыми отчётами в /reports.\n"
        "Будет присылать ссылки сюда."
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer("/start — запустить\n/help — подсказка")
