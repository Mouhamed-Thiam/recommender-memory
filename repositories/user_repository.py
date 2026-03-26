from typing import List, Optional
from models.user import User

class UserRepository:
    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create(self, user: User) -> User:
        user.id = self._next_id
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get_all(self) -> List[User]:
        return list(self._users.values())

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def update(self, user: User) -> User:
        if user.id in self._users:
            self._users[user.id] = user
        return user

    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False