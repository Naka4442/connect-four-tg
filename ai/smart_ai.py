from core import ConnectFour
from typing import Optional
from .igame_ai import IGameAI

class SmartAI(IGameAI):
    """AI, который использует алгоритм Минимакс для принятия решений."""

    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    def make_move(self, game: ConnectFour) -> Optional[int]:
        return self._minimax(game, self.bot_symbol)

    def _minimax(self, game: ConnectFour, symbol: str, depth: int = 3) -> int:
        """Использует алгоритм Минимакс для выбора лучшего хода."""
        best_score = float('-inf')
        best_move = None

        valid_columns = [col for col in range(game.COLS) if game.is_valid_move(col)]
        
        for col in valid_columns:
            temp_game = game.clone()
            temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
            score = self._minimax_score(temp_game, symbol, depth - 1)
            if score > best_score:
                best_score = score
                best_move = col

        return best_move

    def _minimax_score(self, game: ConnectFour, symbol: str, depth: int) -> int:
        """Рекурсивно оценивает игровой процесс."""
        if depth == 0 or game.is_full():
            return self._evaluate_game(game)

        opponent_symbol = game.PLAYER_TOKENS[1] if symbol == self.bot_symbol else self.bot_symbol

        best_score = float('-inf') if symbol == self.bot_symbol else float('inf')

        for col in range(game.COLS):
            if game.is_valid_move(col):
                temp_game = game.clone()
                temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col)
                score = self._minimax_score(temp_game, opponent_symbol, depth - 1)
                if symbol == self.bot_symbol:
                    best_score = max(best_score, score)
                else:
                    best_score = min(best_score, score)

        return best_score

    def _evaluate_game(self, game: ConnectFour) -> int:
        """Оценка текущего состояния игры."""
        if game.check_winner(0, 0):  # Псевдокод для проверки победителя
            return 1  # Победа для бота
        if game.check_winner(1, 0):  # Псевдокод для проверки победителя
            return -1  # Победа для игрока
        return 0  # Ничья