from handlers import StartHandler, GameHandler
from callbacks import GameCallback
from aiogram import Router
from aiogram.filters.command import Command


class MainRouter(Router):
    def __init__(
        self, 
        start_handler: StartHandler,
        game_handler: GameHandler
    ):
        super().__init__()
        self.start_handler = start_handler
        self.game_handler = game_handler
        
    def setup_routes(self):
        self.message.register(self.start_handler.cmd_start_handler, Command("start"))
        self.message.register(self.game_handler.cmd_start_game_handler, Command("start_game"))
        
        self.callback_query.register(self.game_handler.game_callback_handler, GameCallback.filter())