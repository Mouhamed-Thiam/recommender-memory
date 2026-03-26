from dataclasses import dataclass
from typing import Optional

@dataclass
class Item:
    id: Optional[int]
    title: str
    genre: Optional[str]