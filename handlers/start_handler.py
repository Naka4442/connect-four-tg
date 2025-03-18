from aiogram import types


class StartHandler:
    async def cmd_start_handler(self, message: types.Message):
        await message.answer("Добро пожаловать в игру Connect Four! Используйте /start_game чтобы начать игру.")
        
    