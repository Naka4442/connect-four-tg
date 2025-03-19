from core import ConnectFour
from typing import Optional
from .igame_ai import IGameAI

class SmartAI(IGameAI):
    """AI, который использует минимакс для принятия решений."""

    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    def make_move(self, game: ConnectFour) -> Optional[int]:
        player_symbol = game.PLAYER_TOKENS[1]

        # 1. Если бот может выиграть – делаем этот ход
        for col in range(game.COLS):
            if self._can_win_next(game, col, self.bot_symbol):
                return col

        # 2. Если противник может выиграть – блокируем его
        for col in range(game.COLS):
            if self._can_win_next(game, col, player_symbol):
                return col

        # 3. Применяем минимакс для более умного выбора
        return self._minimax(game, self.bot_symbol)

    def _can_win_next(self, game: ConnectFour, col: int, symbol: str) -> bool:
        """Проверяет, можно ли выиграть на следующем ходу."""
        temp_game = game.clone()
        result = temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
        
        if result is None:
            return False  # Если ход невозможен

        row, col = result  # Получаем координаты
        return temp_game.check_winner(row, col)  # Проверяем на победу

    def _minimax(self, game: ConnectFour, symbol: str) -> Optional[int]:
        """Оценка возможных ходов с помощью минимакс."""
        best_score = float('-inf')
        best_move = None

        for col in range(game.COLS):
            if game.is_valid_move(col):
                temp_game = game.clone()
                temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
                score = self._evaluate_game(temp_game, symbol)
                if score > best_score:
                    best_score = score
                    best_move = col

        return best_move

    def _evaluate_game(self, game: ConnectFour, symbol: str) -> int:
        """Оценка позиции для минимакса."""
        if game.check_winner(0, 0):  # Псевдокод для проверки победителя
            return 1 if symbol == self.bot_symbol else -1
        return 0