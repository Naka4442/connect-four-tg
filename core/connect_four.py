class ConnectFour:
    ROWS = 6
    COLS = 7
    EMPTY_CELL = "⬜"
    PLAYER_TOKENS = {1: "🍔", 2: "🌯"}

    def __init__(self):
        self.board = [[self.EMPTY_CELL for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1

    def drop_disc(self, column: int) -> bool:
        """Попытка уронить диск в указанный столбец. Возвращает True, если успешно."""
        if column < 0 or column >= self.COLS or self.board[0][column] != self.EMPTY_CELL:
            return False  # Нельзя сходить в полный или несуществующий столбец
        
        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == self.EMPTY_CELL:
                self.board[row][column] = self.PLAYER_TOKENS[self.current_player]
                if self.check_winner(row, column):
                    return True  # Победа
                self.current_player = 3 - self.current_player  # Переключаем игрока (1 -> 2, 2 -> 1)
                return True
        
        return False

    def check_winner(self, row: int, col: int) -> bool:
        """Проверяет, есть ли победа после последнего хода."""
        token = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Вертикально, горизонтально, 2 диагонали
        
        for dr, dc in directions:
            count = 1
            for sign in (-1, 1):  # Проверяем в обе стороны
                r, c = row + dr * sign, col + dc * sign
                while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == token:
                    count += 1
                    if count >= 4:
                        return True
                    r += dr * sign
                    c += dc * sign
        return False
    
    def is_full(self) -> bool:
        """Проверяет, заполнено ли поле полностью."""
        return all(self.board[0][col] != self.EMPTY_CELL for col in range(self.COLS))

    def render_board(self) -> str:
        """Возвращает строковое представление игрового поля."""
        board_str = "\n".join(" ".join(row) for row in self.board)
        board_str += "\n" + "".join([str(col).center(3) for col in range(1, self.COLS + 1)])
        return board_str

if __name__ == "__main__":
    game = ConnectFour()
    for j in range(6):
        for i in range(7):
            game.drop_disc(i)
    print(game.render_board())