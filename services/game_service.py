from core import ConnectFour
from typing import Dict


class GameService:
    def __init__(self):
        self.games: Dict[int, ConnectFour] = {}  # Храним активные игры (chat_id -> ConnectFour)

    def start_game(self, user_id: int) -> bool:
        """Создаёт новую игру для чата и добавляет первого игрока."""
        if user_id in self.games:
            return False
        self.games[user_id] = ConnectFour()
        return True

    def join_game(self, first_player_id: int, user_id: int) -> str:
        """Добавляет второго игрока в игру."""
        if first_player_id not in self.games:
            if user_id in self.games:
                return "Игра уже запущена!"
            return "Игра не запущена! Используйте /start_game."
        game = self.games[first_player_id]
        

    def make_move(self, chat_id: int, user_id: int, column: int) -> str:
        """Обрабатывает ход игрока."""
        game = self.games.get(chat_id)
        if not game:
            return "Игра не запущена! Используйте /start_game."
        if len(game.players) < 2:
            return "Ожидаем второго игрока."
        
        if not game.drop_disc(user_id, column - 1):
            return "Некорректный ход! Попробуйте снова."
        
        board = game.render_board()
        if game.check_winner(game.ROWS - 1, column - 1):
            del self.games[chat_id]
            return f"{board}\n\nИгрок {game.PLAYER_TOKENS[game.turn % 2 + 1]} победил!"
        
        if game.is_full():
            del self.games[chat_id]
            return f"{board}\n\nНичья!"
        
        return board

    def stop_game(self, chat_id: int) -> str:
        """Останавливает игру в чате."""
        if chat_id in self.games:
            del self.games[chat_id]
            return "Игра завершена."
        return "Нет активной игры."