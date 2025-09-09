from aiogram import Router, types
from .permissions import ALLOWED_USERS

router = Router()


def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USERS


@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    if not is_allowed(message.from_user.id):
        return
    await message.answer("Бот следит за новыми отчётами в /reports.\n"
                         "Будет присылать ссылки сюда.")


@router.message(commands=["help"])
async def cmd_help(message: types.Message):
    if not is_allowed(message.from_user.id):
        return
    await message.answer("/start — запустить\n/help — подсказка")
