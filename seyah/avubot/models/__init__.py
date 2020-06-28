from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Platform(Enum):
    DISCORD = "discord"
    TWITCH = "twitch"


@dataclass
class GameUser():
    id: int
    discord: Optional[str]
    twitch: Optional[str]
    game_id: Optional[str]
