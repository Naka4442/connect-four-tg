from services import GameService
from aiogram import types


class StartHandler:
    def __init__(self, game_service: GameService):
        self.game_service = game_service
        
    async def cmd_start_handler(self, message: types.Message):
        await message.answer("Добро пожаловать в игру Connect Four! Используйте /start_game чтобы начать игру.")
        
    