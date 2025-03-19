from abc import ABC, abstractmethod
from core import ConnectFour
from typing import Optional


class IGameAI(ABC):
    @abstractmethod
    def make_move(self, game: ConnectFour) -> Optional[int]:
        """Определяет, в какой столбец сходить боту."""
        pass