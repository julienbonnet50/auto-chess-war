from enum import Enum


class BattleState(Enum):
    SETUP = "setup"
    ONGOING = "ongoing"
    VICTORY = "victory"
    DEFEAT = "defeat"
    DRAW = "draw"