from dataclasses import dataclass


@dataclass
class PlayerData:
    name: str
    block_game: int | None
    description: str
