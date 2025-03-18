from services import GameService
from aiogram import types


class RestartHandler:
    def __init__(self, game_service: GameService):
        self.game_service = game_service
        
    async def cmd_restart_handler(self, message: types.Message):
        if not self.game_service.stop_game(message.from_user.id):
            await message.reply("У вас нет активной игры! Начните игру с помощью /game !")
            return
        await message.reply("Игра успешно удалена!")