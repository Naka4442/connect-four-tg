from typing import Optional
from enum import Enum


class GameStatus(Enum):
    ONGOING = "ongoing"
    WIN = "win"
    DRAW = "draw"
    INVALID_MOVE = "invalid_move"


class GameResult:
    def __init__(self, status: GameStatus, winner: Optional[str] = None):
        self.status = status
        self.winner = winner