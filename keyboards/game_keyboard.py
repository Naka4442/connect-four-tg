from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import GameCallback
from typing import List


class GameKeyboard:
    def get_keyboard(self, board: List[List[str]], first_player_id: int):
        builder = InlineKeyboardBuilder()
        for i in range(1, 8):
            builder.button(text="🔽", callback_data=GameCallback(col_index=i, first_player_id=first_player_id))
        for row in board:
            for cell in row:
                builder.button(text=cell, callback_data=GameCallback(col_index=-1))
        builder.adjust(7)
        return builder.as_markup()
    