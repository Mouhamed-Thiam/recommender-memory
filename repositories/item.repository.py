from typing import List, Optional
from models.item import Item

class ItemRepository:
    def __init__(self):
        self._items: dict[int, Item] = {}
        self._next_id = 1

    def create(self, item: Item) -> Item:
        item.id = self._next_id
        self._items[item.id] = item
        self._next_id += 1
        return item

    def get_all(self) -> List[Item]:
        return list(self._items.values())

    def get_by_id(self, item_id: int) -> Optional[Item]:
        return self._items.get(item_id)

    def update(self, item: Item) -> Item:
        if item.id in self._items:
            self._items[item.id] = item
        return item

    def delete(self, item_id: int) -> bool:
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False