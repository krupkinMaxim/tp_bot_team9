import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from aiogram import Router
from aiogram.types import CallbackQuery

# Фикстуры в pytest позволяют выносить в отдельные функции типовые действия
# например: настройка тестового окружения, создание тестовых данных, выполнение завершающие действия
# https://habr.com/ru/articles/731296/

@pytest.fixture
def mock_bot():
    """Моск бот"""
    with patch("main.Bot") as mock_bot_cls:
        mock_bot_instance = AsyncMock()
        mock_bot_cls.return_value = mock_bot_instance
        yield mock_bot_instance

@pytest.fixture()
def mock_set_commands():
    """Mock создание меню"""
    with patch("main.set_commands", new_callable=AsyncMock) as mock:
        yield mock_set_commands


def mock_set_up_logger():
    """Mock логер """
    with patch("main.set_up_logger", new_callable=AsyncMock) as mock:
        yield mock_set_up_logger



@pytest.fixture
def mock_dispatcher():
    """Моск диспетчер"""
    with patch("main.Dispatcher") as mock_dispatcher_cls:
        mock_dispatcher_instance = AsyncMock()
        mock_dispatcher_instance.start_polling = AsyncMock()
        mock_dispatcher_instance.include_routers = AsyncMock()
        mock_dispatcher_cls.return_value = mock_dispatcher_instance
        yield mock_dispatcher_instance



@pytest.fixture
def mock_message():
    """Mock сообщение"""
    mock_msg = AsyncMock(spec=Message)
    mock_msg.answer = AsyncMock()
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.username = AsyncMock()
    return mock_msg


@pytest.fixture
def mock_callback(mock_message):
    """Создает мок объекта CallbackQuery с прикрепленным моком Message"""
    callback = AsyncMock(spec=CallbackQuery)
    callback.message = mock_message
    return callback


@pytest.fixture
def mock_router():
    """Mock роутер"""
    router = Router()
    return router