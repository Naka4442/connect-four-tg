from typing import List, Optional
from enum import Enum


class GameStatus(Enum):
    ONGOING = "ongoing"
    WIN = "win"
    DRAW = "draw"
    INVALID_MOVE = "invalid_move"


class GameResult:
    def __init__(
            self, 
            status: GameStatus, 
            game_state: Optional[List[List[str]]] = None,
            winner: Optional[str] = None
        ):
        self.game_state = game_state
        self.status = status
        self.winner = winner