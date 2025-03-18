from  core import ConnectFour, ConnectFourAI, GameStatus, GameResult
from typing import Optional, Dict
import asyncio


class AIGameService:
    def __init__(self):
        self.games: Dict[int, ConnectFour] = {}
        self.ai = None  # Инициализация ИИ

    def start_game(self, user_id: int) -> bool:
        """Создаёт новую игру для пользователя и добавляет игрока."""
        if user_id in self.games:
            return False
        self.games[user_id] = ConnectFour()
        self.ai = ConnectFourAI(bot_symbol="AI", player_symbol="X")  # Инициализируем ИИ
        return True

    def make_move(self, user_id: int, column: int) -> GameResult:
        """Делает ход игрока и ход бота."""
        game = self.games.get(user_id)
        if not game:
            return GameResult(GameStatus.INVALID_MOVE)

        # Игрок делает ход
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

        # Ход бота с задержкой
        asyncio.run(self.bot_move(user_id, game))  # Добавляем асинхронный ход бота

        if game.check_winner(row, col):
            del self.games[user_id]
            return GameResult(GameStatus.WIN, "AI")  # Бот победил

        if game.is_full():
            del self.games[user_id]
            return GameResult(GameStatus.DRAW)

        return GameResult(GameStatus.ONGOING)

    async def bot_move(self, user_id: int, game: ConnectFour):
        """Асинхронный ход бота, делаем задержку, чтобы бот "подумал"."""
        await asyncio.sleep(2)  # Задержка, имитирующая раздумья бота
        bot_column = self.ai.make_move(game.board)
        if bot_column != -1:
            game.drop_disc("AI", bot_column)

    def get_active_player(self, user_id: int) -> Optional[str]:
        """Возвращает текущего активного игрока."""
        game = self.games.get(user_id)
        if not game:
            return None
        return game.PLAYER_TOKENS.get(game.turn % 2 + 1)

    def stop_game(self, user_id: int) -> bool:
        """Останавливает игру."""
        if user_id in self.games:
            del self.games[user_id]
            return True
        return False