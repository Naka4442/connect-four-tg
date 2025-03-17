from aiogram.filters.callback_data import CallbackData


class GameCallback(CallbackData, prefix="game"):
    col_index: int
