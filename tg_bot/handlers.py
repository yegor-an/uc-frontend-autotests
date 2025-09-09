from aiogram import Router, types
from .config import ALLOWED_USERS

router = Router()


@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer(
        "Бот следит за новыми отчётами в /reports.\n"
        "Будет присылать ссылки сюда."
    )


@router.message(commands=["help"])
async def cmd_help(message: types.Message):
    if message.from_user.id not in ALLOWED_USERS:
        return
    await message.answer("/start — запустить\n/help — подсказка")
