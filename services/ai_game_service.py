from  core import ConnectFour, ConnectFourAI, GameStatus, GameResult
from typing import Optional, Dict
import asyncio


class AIGameService:
    def __init__(self):
        self.games: Dict[int, ConnectFour] = {}
        self.ai = None

    def start_game(self, user_id: int) -> bool:
        if user_id in self.games:
            return False
        game = ConnectFour()
        game.add_player(user_id)
        game.add_player(0)
        self.games[user_id] = game
        self.ai = ConnectFourAI(bot_symbol="🤖", player_symbol=game.PLAYER_TOKENS[1])
        return True

    def make_move(self, user_id: int, column: int) -> GameResult:
        game = self.games.get(user_id)
        if not game:
            return GameResult(GameStatus.INVALID_MOVE)

        move = game.drop_disc(user_id, column - 1)
        if move is None:
            return GameResult(GameStatus.INVALID_MOVE)

        row, col = move
        if game.check_winner(row, col):
            del self.games[user_id]
            return GameResult(GameStatus.WIN, user_id)

        if game.is_full():
            del self.games[user_id]
            return GameResult(GameStatus.DRAW)

        return GameResult(GameStatus.ONGOING)

    def bot_move(self, user_id: int) -> GameResult:
        game = self.games.get(user_id)
        if not game:
            return GameResult(GameStatus.INVALID_MOVE)

        bot_column = self.ai.make_move(game.board)
        if bot_column == -1:
            return GameResult(GameStatus.DRAW)

        move = game.drop_disc(0, bot_column)
        if move is None:
            return GameResult(GameStatus.INVALID_MOVE)

        row, col = move
        if game.check_winner(row, col):
            del self.games[user_id]
            return GameResult(GameStatus.WIN, "AI")

        if game.is_full():
            del self.games[user_id]
            return GameResult(GameStatus.DRAW)

        return GameResult(GameStatus.ONGOING)

    def get_active_player(self, user_id: int) -> str:
        game = self.games.get(user_id)
        return game.PLAYER_TOKENS[game.turn % 2 + 1] if game else "?"