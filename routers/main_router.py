from handlers import *
from callbacks import GameCallback
from aiogram import Router
from aiogram.filters.command import Command


class MainRouter(Router):
    def __init__(
        self, 
        start_handler: StartHandler,
        game_handler: GameHandler,
        ai_game_handler: AIGameHandler,
        restart_handler: RestartHandler
    ):
        super().__init__()
        self.start_handler = start_handler
        self.game_handler = game_handler
        self.ai_game_handler = ai_game_handler
        self.restart_handler = restart_handler
        
    def setup_routes(self):
        self.message.register(self.start_handler.cmd_start_handler, Command("start"))
        self.message.register(self.game_handler.cmd_start_game_handler, Command("game"))
        self.message.register(self.ai_game_handler.cmd_start_game_handler, Command("ai_game"))
        self.message.register(self.restart_handler.cmd_restart_handler, Command("restart"))
        
        self.callback_query.register(self.game_handler.game_callback_handler, GameCallback.filter())