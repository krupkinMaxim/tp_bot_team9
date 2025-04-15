import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN
from handlers.bot_commands import set_commands
from handlers import router


# функция запуска проекта
async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(router)

    # вызов меню  команд
    await set_commands(bot=bot)

    # поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())