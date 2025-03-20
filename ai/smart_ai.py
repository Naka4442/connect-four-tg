from core import ConnectFour
from typing import Optional
from .igame_ai import IGameAI


class SmartAI(IGameAI):
    """AI, который анализирует поле, предотвращает проигрыш и строит стратегию."""

    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol  # Символ бота

    def make_move(self, game: ConnectFour) -> Optional[int]:
        player_symbol = next(symbol for symbol in game.PLAYER_TOKENS.values() if symbol != self.bot_symbol)

        # 1. Если бот может выиграть – делаем этот ход
        for col in range(game.COLS):
            if self._can_win_next(game, col, self.bot_symbol):
                return col

        # 2. Если игрок может выиграть в 1 ход – блокируем
        for col in range(game.COLS):
            if self._can_win_next(game, col, player_symbol):
                return col

        # 3. Если игрок создаёт "ловушку" (выигрыш через 2 хода), блокируем
        for col in range(game.COLS):
            if self._is_trap_move(game, col, player_symbol):
                return col

        # 4. Проверяем, какие ходы создают опасные ситуации (например, 3 в ряд внизу)
        for col in range(game.COLS):
            if self._is_critical_threat(game, col, player_symbol):
                return col

        # 5. Выбираем лучший стратегический ход
        return self._choose_best_move(game)

    def _can_win_next(self, game: ConnectFour, col: int, symbol: str) -> bool:
        """Проверяет, можно ли выиграть на следующем ходу."""
        if not game.is_valid_move(col):
            return False

        temp_game = game.clone()
        player_id = self._get_player_id(game, symbol)
        result = temp_game.drop_disc(player_id, col)

        if result is None:
            return False

        row, col = result
        return temp_game.check_winner(row, col)

    def _is_trap_move(self, game: ConnectFour, col: int, player_symbol: str) -> bool:
        """Проверяет, создаёт ли ход угрозу проигрыша через 2 хода."""
        if not game.is_valid_move(col):
            return False

        temp_game = game.clone()
        player_id = self._get_player_id(game, player_symbol)
        result = temp_game.drop_disc(player_id, col)

        if result is None:
            return False

        # После этого хода проверяем, есть ли у игрока выигрышная комбинация через 1 ход
        for next_col in range(game.COLS):
            if self._can_win_next(temp_game, next_col, player_symbol):
                return True

        return False

    def _is_critical_threat(self, game: ConnectFour, col: int, player_symbol: str) -> bool:
        """Проверяет, создаёт ли ход ситуацию, в которой противник почти выигрывает."""
        if not game.is_valid_move(col):
            return False

        temp_game = game.clone()
        player_id = self._get_player_id(game, player_symbol)
        result = temp_game.drop_disc(player_id, col)

        if result is None:
            return False

        row, col = result

        # Проверяем, если у игрока уже 3 в ряд снизу – это критическая угроза
        return temp_game.count_in_a_row(row, col, player_symbol) == 3

    def _choose_best_move(self, game: ConnectFour) -> Optional[int]:
        """Выбирает лучший ход, анализируя возможные комбинации."""
        valid_columns = [col for col in range(game.COLS) if game.is_valid_move(col)]

        # Оцениваем стратегические позиции: центр + боковые комбинации
        best_cols = sorted(valid_columns, key=lambda x: (abs(x - game.COLS // 2), -self._column_height(game, x)))

        return best_cols[0] if best_cols else None

    def _column_height(self, game: ConnectFour, col: int) -> int:
        """Возвращает, насколько высоко уже сложены фишки в колонке (чтобы не строить башню)."""
        for row in range(game.ROWS):
            if game.board[row][col] == " ":
                return row
        return game.ROWS

    def _get_player_id(self, game: ConnectFour, symbol: str) -> int:
        """Получает ID игрока по символу."""
        return next(uid for uid, token in game.players.items() if game.PLAYER_TOKENS[token] == symbol)