import pytest
from main import main
from fixtures import mock_bot, mock_dispatcher, mock_set_commands , mock_router, mock_set_up_logger

@pytest.mark.asyncio
async def test_main(mock_bot, mock_dispatcher, mock_router, mock_set_commands, mock_set_up_logger):
    # вызов функции main
    await main()

   # Проверка
mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)
mock_dispatcher.include_routers.assert_awaited_once_with(mock_router)
mock_set_commands.assert_awaited_once_with(mock_bot)
mock_set_up_logger.asseert_awaited_once()


# TODO- ДОДЕЛАТЬ ВЫЗОВ ФУНКЦИИ