__all__ = [

    'router'
]
# TODO - Опишите вызов функций обработчиков через маршрутизацию
# Работа c Router - https://docs.aiogram.dev/en/v3.14.0/dispatcher/router.html
# Пример работы с Router через декораторы @router - https://mastergroosha.github.io/aiogram-3-guide/routers/
# Пример работы с Router через функцию сборщик https://stackoverflow.com/questions/77809738/how-to-connect-a-router-in-aiogram-3-x-x#:~:text=1-,Answer,-Sorted%20by%3A

from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject
from .keyboard import main_keyboard   # импорт из клавиатур
from .callbacks import callback_message  # импорт из коллбека
from config import CMC_API_KEY
import requests
import aiohttp

router = Router()


@router.message(Command("price"))
async def price_handler(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("❗ Пожалуйста, укажи тикер токена после команды, например:\n/price bitcoin")
        return

    token = command.args.lower()

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": token,
        "vs_currencies": "usd"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                await message.answer("❌ Не удалось получить данные от CoinGecko.")
                return
            data = await resp.json()

    price = data.get(token, {}).get("usd")

    if price is None:
        await message.answer(f"❌ Не найден токен с названием '{token}'. Проверь правильность написания.")
    else:
        await message.answer(f"💰 Цена {token.upper()}: ${price:.4f}")

@router.message(Command("start"))
async def process_start_command(message: types.Message):
    await message.answer(
        f"""
👋 Привет, {message.from_user.first_name}!

Я — твой крипто-помощник на каждый день.

🪙 Помогу тебе быстро узнать актуальные цены ключевых криптовалют.
📈 Покажу топ монет, расскажу об изменениях за день и помогу следить за курсом.
🔔 Скоро сможешь даже установить уведомления на нужную цену!

Просто напиши команду или воспользуйся меню.
Если не знаешь с чего начать — отправь /help 💡
"""
    )
@router.message(Command("help"))
async def process_help_command(message: types.Message):
    await message.answer(text="""
 Что я умею?:

Привет! Я — твой крипто-помощник, и вот список команд, которые тебе доступны:

⸻

📍 Основные команды:

🔹 /start — краткое знакомство со мной и моими возможностями.
🔹 /help — показать это меню помощи.

💰 /daily — цены на топ-5 криптовалют  
💲 /price <токен> — узнать текущую цену токена  
📉 /change <токен> — изменение цены токена за 24 часа

Примеры:  
/price bitcoin  
/change solana
⸻

Если не знаешь, с чего начать — просто отправь /daily 
Скоро добавим ещё больше функций! 🚀""", reply_markup= main_keyboard)


@router.message(Command("daily"))
async def daily_handler(message: types.Message):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 5,
        "page": 1,
        "sparkline": "false"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    await message.answer("❌ Не удалось получить данные от CoinGecko.")
                    return
                data = await resp.json()
    except Exception as e:
        await message.answer(f"❌ Ошибка при запросе данных: {e}")
        return

    msg = "🔥 Цена топ 5 криптовалют на сегодня :\n\n"
    for coin in data:
        name = coin.get('name', 'N/A')
        symbol = coin.get('symbol', 'N/A').upper()
        price = coin.get('current_price', 0)
        change = coin.get('price_change_percentage_24h', 0)
        msg += f"{name} ({symbol}): ${price:.2f} ({change:+.2f}%)\n"

    await message.answer(msg)


@router.message(Command("testkey"))
async def test_api_key_handler(message: types.Message):
    if not CMC_API_KEY:
        await message.answer("⚠️ API ключ не найден! Проверь файл .env и переменную CMC_API_KEY.")
        return

    await message.answer(f"🔑 Текущий API ключ:\n`{CMC_API_KEY}`", parse_mode="Markdown")

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }
    params = {
        "start": "1",
        "limit": "1",
        "convert": "USD"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Отправим в ответ название и цену первой криптовалюты
        first_crypto = data["data"][0]
        name = first_crypto["name"]
        price = first_crypto["quote"]["USD"]["price"]

        await message.answer(f"✅ Запрос успешен!\nПервая криптовалюта: {name}\nЦена: ${price:.2f}")

    except requests.exceptions.RequestException as e:
        await message.answer(f"❌ Ошибка при запросе к CoinMarketCap:\n{e}")

@router.message(Command("change"))
async def change_handler(message: types.Message, command: CommandObject):
    if not command.args:
        await message.answer("📩 Укажи название токена, например:\n`/change ethereum`", parse_mode="Markdown")
        return

    token = command.args.lower()
    url = f"https://api.coingecko.com/api/v3/coins/{token}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await message.answer("❌ Не удалось найти токен. Попробуй другой.")
                    return
                data = await resp.json()

        current_price = data["market_data"]["current_price"]["usd"]
        price_24h_ago = current_price / (1 + (data["market_data"]["price_change_percentage_24h"] / 100))
        change_pct = data["market_data"]["price_change_percentage_24h"]
        change_abs = current_price - price_24h_ago

        arrow = "📈" if change_pct > 0 else "📉"

        msg = (
            f"{arrow} *{data['name']}* за 24ч:\n"
            f"Вчера: ${price_24h_ago:.2f}\n"
            f"Сейчас: ${current_price:.2f}\n"
            f"Изменение: {change_pct:+.2f}% (${change_abs:+.2f})"
        )
        await message.answer(msg, parse_mode="Markdown")

    except Exception as e:
        await message.answer("⚠️ Ошибка при получении данных.")
        print(e)

# Здесь описывается маршрутизация
def register_message_handlers():
    '''Маршрутизация обработчиков'''
    pass
