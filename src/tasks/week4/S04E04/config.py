from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Config:
    PORT: int = 5111
    MAP_DESCRIPTION: Dict[str, str] = field(default_factory=lambda: {
        "0:0": "start",
        "0:1": "trawa",
        "0:2": "trawa drzewo",
        "0:3": "dom",
        "1:0": "trawa",
        "1:1": "wiatrak",
        "1:2": "trawa",
        "1:3": "trawa",
        "2:0": "trawa",
        "2:1": "trawa",
        "2:2": "kamienie",
        "2:3": "dwa drzewa",
        "3:0": "góry",
        "3:1": "góry",
        "3:2": "auto",
        "3:3": "jaskinia"
    })