from dataclasses import dataclass
from typing import Optional

@dataclass
class Rating:
    id: Optional[int]
    user_id: int
    item_id: int
    rating: int