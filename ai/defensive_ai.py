from core import ConnectFour
from typing import Optional
from .igame_ai import IGameAI
import random


class DefensiveAI(IGameAI):
    """AI, который блокирует победный ход игрока."""

    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    def make_move(self, game: ConnectFour) -> Optional[int]:
        player_symbol = game.PLAYER_TOKENS[1]

        # 1. Блокируем победный ход противника
        for col in range(game.COLS):
            if self._can_win_next(game, col, player_symbol):
                return col

        # 2. Если нет угрозы, выбираем столбец по стратегии
        return self._choose_best_move(game)

    def _can_win_next(self, game: ConnectFour, col: int, symbol: str) -> bool:
        """Проверяет, может ли противник выиграть на следующем ходу."""
        temp_game = game.clone()
        result = temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
        
        if result is None:
            return False  # Если ход невозможен

        row, col = result  # Получаем координаты
        return temp_game.check_winner(row, col)  # Проверяем на победу

    def _choose_best_move(self, game: ConnectFour) -> int:
        """Выбирает лучший ход на основе анализа поля."""
        valid_columns = [col for col in range(game.COLS) if game.is_valid_move(col)]
        
        # Простой случайный выбор среди доступных колонок (можно улучшить)
        return random.choice(valid_columns) if valid_columns else None
    