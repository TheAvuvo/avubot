from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Platform(Enum):
    DISCORD = "DISCORD"
    TWITCH = "TWITCH"

    def __str__(self):
        return self.value


class Game(Enum):
    ROCKETLEAGUE = ("ROCKETLEAGUE", "rl")
    VALORANT = ("VALORANT", "valorant")
    JACKBOX = ("JACKBOX", "jackbox")

    @classmethod
    def to_enum(cls, game: str) -> Optional["Game"]:
        if game == "ROCKETLEAGUE":
            return Game.ROCKETLEAGUE
        elif game == "VALORANT":
            return Game.VALORANT
        elif game == "JACKBOX":
            return Game.JACKBOX
        else:
            return None

    def __str__(self):
        return self.value[0]

    def cmd(self):
        return self.value[1]


@dataclass
class GameUser():
    uid: int
    username: str
    platform: Platform
    game: Game
    game_id: str
