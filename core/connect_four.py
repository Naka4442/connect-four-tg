from typing import Optional


class ConnectFour:
    ROWS = 6
    COLS = 7
    EMPTY_CELL = "⚫️"
    PLAYER_TOKENS = {1: "💩", 2: "❤️"}

    def __init__(self):
        self.board = [[self.EMPTY_CELL for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.players = {}  # {user_id: player_number}
        self.turn = 0  # Количество ходов (определяет, чей ход)

    def add_player(self, user_id: int) -> bool:
        if user_id not in self.players and len(self.players) < 2:
            self.players[user_id] = len(self.players) + 1
            return True
        return False

    def drop_disc(self, user_id: int, column: int) -> Optional[tuple[int, int]]:
        if user_id not in self.players or self.players[user_id] != self.turn % 2 + 1:
            return None
        if column < 0 or column >= self.COLS or self.board[0][column] != self.EMPTY_CELL:
            return None

        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == self.EMPTY_CELL:
                self.board[row][column] = self.PLAYER_TOKENS[self.players[user_id]]
                self.turn += 1
                return row, column  # Возвращаем позицию последнего хода
        return None

    def check_winner(self, row: int, col: int) -> bool:
        token = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        if token == self.EMPTY_CELL: return
        for dr, dc in directions:
            count = 1
            for sign in (-1, 1):
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == token:
                    count += 1
                    if count >= 4:
                        return True
                    r += dr * sign
                    c += dc * sign
        return False
    
    def is_full(self) -> bool:
        return all(self.board[0][col] != self.EMPTY_CELL for col in range(self.COLS))

    def render_board(self) -> str:
        board_str = "\n".join("".join(row) for row in self.board)
        return board_str