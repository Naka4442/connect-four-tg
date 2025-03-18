import random
from typing import List, Optional


class ConnectFourAI:
    def __init__(self, bot_symbol: str, player_symbol: str):
        self.bot_symbol = bot_symbol
        self.player_symbol = player_symbol

    def make_move(self, board: List[List[Optional[str]]]) -> int:
        """Выбирает столбец для хода бота."""
        # 1. Проверить, есть ли победный ход для бота
        for col in range(len(board[0])):
            if self._can_win_next(board, col, self.bot_symbol):
                return col

        # 2. Проверить, не побеждает ли игрок на следующем ходу
        for col in range(len(board[0])):
            if self._can_win_next(board, col, self.player_symbol):
                return col  # Заблокировать игрока

        # 3. Если нет критичных ходов, выбираем случайный допустимый ход
        valid_columns = [col for col in range(len(board[0])) if board[0][col] is None]
        return random.choice(valid_columns) if valid_columns else -1  # Если доска заполнена

    def _can_win_next(self, board: List[List[Optional[str]]], col: int, symbol: str) -> bool:
        """Проверяет, может ли кто-то выиграть на следующем ходу."""
        temp_board = [row[:] for row in board]  # Копируем доску
        for row in reversed(temp_board):
            if row[col] is None:
                row[col] = symbol
                return self._check_win(temp_board, symbol)
        return False

    def _check_win(self, board: List[List[Optional[str]]], symbol: str) -> bool:
        """Проверяет, есть ли выигрышная комбинация на доске."""
        rows, cols = len(board), len(board[0])

        def check_direction(x, y, dx, dy):
            """Проверяет 4 подряд в заданном направлении."""
            count = 0
            for _ in range(4):
                if 0 <= x < rows and 0 <= y < cols and board[x][y] == symbol:
                    count += 1
                    x += dx
                    y += dy
                else:
                    break
            return count == 4

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == symbol:
                    if (check_direction(r, c, 1, 0) or  # Вертикально
                        check_direction(r, c, 0, 1) or  # Горизонтально
                        check_direction(r, c, 1, 1) or  # Диагональ \
                        check_direction(r, c, 1, -1)):  # Диагональ /
                        return True
        return False