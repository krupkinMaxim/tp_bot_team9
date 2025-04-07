import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN

# тест
from handlers import set_commands

# Экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

#Бот принимает команды, например /start.
# Создадим хендлер - обработчик сообщений, и будем возвращать сообщение
@dp.message(Command('start'))
async def process_start_command(message):
  await message.answer("Привет!")


@dp.message()
async def echo_message(message):
    await message.answer(message.text)

# функция запуска проекта
async def main():

    # вызов меню команд
    await set_commands(bot=bot)

    # поллинг
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())