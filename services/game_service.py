from core import ConnectFour, GameResult, GameStatus
from typing import Dict


class GameService:
    def __init__(self):
        self.games: Dict[int, ConnectFour] = {}

    def start_game(self, user_id: int) -> bool:
        """Создаёт новую игру для чата и добавляет первого игрока."""
        if user_id in self.games:
            return False
        self.games[user_id] = ConnectFour()
        print(self.games)
        return True

    def join_game(self, first_player_id: int, user_id: int) -> str:
        """Добавляет второго игрока в игру."""
        game = self.games.get(first_player_id)
        if not game:
            return "Игра не запущена! Используйте /game."
        if not game.add_player(user_id):
            return "В игру уже вошли два игрока."
        return "Второй игрок вошел в игру."
        

    def make_move(self, first_player_id: int, user_id: int, column: int) -> GameResult:
        game = self.games.get(first_player_id)
        if not game:
            return GameResult(GameStatus.INVALID_MOVE)

        if len(game.players) < 2:
            self.join_game(first_player_id, user_id)

        potentional_winner = self.get_active_player(first_player_id)
        move = game.drop_disc(user_id, column - 1)
        if move is None:
            return GameResult(GameStatus.INVALID_MOVE)

        row, col = move
        if game.check_winner(row, col):
            del self.games[first_player_id]
            return GameResult(GameStatus.WIN, potentional_winner)

        if game.is_full():
            del self.games[first_player_id]
            return GameResult(GameStatus.DRAW)

        return GameResult(GameStatus.ONGOING)

    def get_active_player(self, first_player_id: int) -> str | None:
        game = self.games.get(first_player_id)
        if not game:
            return None
        return game.PLAYER_TOKENS.get(game.turn % 2 + 1)

    def stop_game(self, first_player_id: int) -> bool:
        """Останавливает игру в чате."""
        if first_player_id in self.games:
            del self.games[first_player_id]
            return True
        return False
