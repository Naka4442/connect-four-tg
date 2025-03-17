from handlers import StartHandler
from aiogram import Router
from aiogram.filters.command import Command


class MainRouter(Router):
    def __init__(self, start_handler: StartHandler):
        super().__init__()
        self.start_handler = start_handler
        
    def setup_routes(self):
        self.message.register(self.start_handler.cmd_start_handler, Command("start"))