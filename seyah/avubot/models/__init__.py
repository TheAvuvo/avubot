from dataclasses import dataclass
from enum import Enum


class Platform(Enum):
    DISCORD = "DISCORD"
    TWITCH = "TWITCH"

    def __str__(self):
        return self.value


class Game(Enum):
    ROCKETLEAGUE = ("ROCKETLEAGUE", "rl")
    VALORANT = ("VALORANT", "valorant")
    JACKBOX = ("JACKBOX", "jackbox")

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
