from core import ConnectFour
from typing import Optional
from .igame_ai import IGameAI
import random


class DefensiveAI(IGameAI):
    """AI, который пытается заблокировать победный ход противника."""

    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    def make_move(self, game: ConnectFour) -> Optional[int]:
        player_symbol = game.PLAYER_TOKENS[1]

        # 1. Блокирует победный ход противника
        for col in range(game.COLS):
            if self._can_win_next(game, col, player_symbol):
                return col

        # 2. Если нет угрозы, выбираем случайный ход
        valid_columns = [col for col in range(game.COLS) if game.is_valid_move(col)]
        return random.choice(valid_columns) if valid_columns else None

    def _can_win_next(self, game: ConnectFour, col: int, symbol: str) -> bool:
        """Проверяет, может ли противник выиграть на следующем ходу."""
        temp_game = game.clone()
        result = temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
        
        if result is None:
            return False  # Если ход невозможен

        row, col = result  # Получаем координаты
        return temp_game.check_winner(row, col)  # Проверяем на победу