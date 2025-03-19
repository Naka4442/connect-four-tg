import random
from core import ConnectFour
from typing import Optional
from ai import IGameAI


class ConnectFourAI(IGameAI):
    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    def make_move(self, game: ConnectFour) -> Optional[int]:
        """Выбирает оптимальный ход бота."""
        # 1. Если есть победный ход – сделаем его
        for col in range(game.COLS):
            if self._can_win_next(game, col, self.bot_symbol):
                return col

        # 2. Если игрок может выиграть – блокируем
        player_symbol = game.PLAYER_TOKENS[1]
        for col in range(game.COLS):
            if self._can_win_next(game, col, player_symbol):
                return col

        # 3. Выбираем случайный допустимый ход
        valid_columns = [col for col in range(game.COLS) if game.is_valid_move(col)]
        return random.choice(valid_columns) if valid_columns else None

    def _can_win_next(self, game: ConnectFour, col: int, symbol: str) -> bool:
        """Проверяет, можно ли выиграть на следующем ходу."""
        temp_game = game.clone()  # Копируем игру (метод клонирования нужно добавить в ConnectFour)
        return temp_game.drop_disc(0 if symbol == self.bot_symbol else 1, col) is not None and temp_game.check_winner()
