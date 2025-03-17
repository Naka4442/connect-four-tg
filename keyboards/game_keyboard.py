from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import GameCallback


class GameKeyboard:
    def __init__(self):
        self.builder = InlineKeyboardBuilder()
        
    def get_keyboard(self):
        for i in range(1, 8):
            self.builder.button(text=f"{i}", callback_data=GameCallback(col_index=i))
        return self.builder.as_markup()
    