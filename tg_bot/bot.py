import asyncio
from aiogram import Bot, Dispatcher
from bot_config import TELEGRAM_TOKEN
from handlers import router
from watcher import ReportsWatcher


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    watcher = ReportsWatcher(bot, interval=15)

    await asyncio.gather(
        dp.start_polling(bot),
        watcher.run()
    )


if __name__ == "__main__":
    asyncio.run(main())
