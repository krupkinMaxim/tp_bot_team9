from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot):
    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='help', description='Справка'),
        BotCommand(command='daily', description='Цена ключевых активов'),
        BotCommand(command='price', description='Узнать цену любого актива'),
        BotCommand(command='change', description='Узнать изменение цены за 24 часа'),

                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
