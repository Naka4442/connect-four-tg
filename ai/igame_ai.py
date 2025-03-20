from abc import ABC, abstractmethod
from core import ConnectFour
from typing import Optional


class IGameAI(ABC):
    def __init__(self, bot_symbol: str):
        self.bot_symbol = bot_symbol

    @abstractmethod
    def make_move(self, game: ConnectFour) -> Optional[int]:
        """Определяет, в какой столбец сходить боту."""
        pass