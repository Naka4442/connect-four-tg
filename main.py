from aiogram import Bot, Dispatcher
from services import GameService
from routers import MainRouter
from handlers import *
from keyboards import GameKeyboard
from utils import load_config
import asyncio



async def main():
    # telegram
    config = load_config()
    bot = Bot(token=config["bot"]["token"])
    dp = Dispatcher()
    # core
    game_service = GameService()
    game_keyboard = GameKeyboard()
    start_handler = StartHandler()
    game_handler = GameHandler(game_service, game_keyboard)
    restart_handler = RestartHandler(game_service)
    main_router = MainRouter(
        start_handler, 
        game_handler,
        restart_handler
    )
    main_router.setup_routes()
    dp.include_router(main_router)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())