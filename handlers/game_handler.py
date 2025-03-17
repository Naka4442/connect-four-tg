from services import GameService
from aiogram import types


class GameHandler:
    def __init__(self, game_service: GameService):
        self.game_service = game_service
        
    def cmd_start_game_handler(self, message: types.Message):
        ...