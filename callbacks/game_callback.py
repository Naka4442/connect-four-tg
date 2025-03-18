from aiogram.filters.callback_data import CallbackData
from typing import Optional


class GameCallback(CallbackData, prefix="game"):
    col_index: int
    first_player_id: Optional[int] = None

class AIGameCallback(CallbackData, prefix="game"):
    col_index: int