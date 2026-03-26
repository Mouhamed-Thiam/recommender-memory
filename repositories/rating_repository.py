from typing import Dict, List, Optional
from models.rating import Rating

class RatingRepository:
    def __init__(self):
        self._ratings: dict[int, Rating] = {}
        self._next_id = 1
        # Index pour accélérer les requêtes
        self._user_ratings: dict[int, dict[int, int]] = {}  # user_id -> {item_id: rating}
        self._item_ratings: dict[int, dict[int, int]] = {}  # item_id -> {user_id: rating}

    def create(self, rating: Rating) -> Rating:
        rating.id = self._next_id
        self._ratings[rating.id] = rating
        self._next_id += 1

        # Mise à jour des index
        if rating.user_id not in self._user_ratings:
            self._user_ratings[rating.user_id] = {}
        self._user_ratings[rating.user_id][rating.item_id] = rating.rating

        if rating.item_id not in self._item_ratings:
            self._item_ratings[rating.item_id] = {}
        self._item_ratings[rating.item_id][rating.user_id] = rating.rating

        return rating

    def get_ratings_by_user(self, user_id: int) -> Dict[int, int]:
        """Retourne un dictionnaire item_id -> rating pour l'utilisateur."""
        return self._user_ratings.get(user_id, {}).copy()

    def get_ratings_by_item(self, item_id: int) -> Dict[int, int]:
        """Retourne un dictionnaire user_id -> rating pour l'item."""
        return self._item_ratings.get(item_id, {}).copy()

    def get_all(self) -> List[Rating]:
        return list(self._ratings.values())

    def delete_by_user(self, user_id: int) -> None:
        """Supprime toutes les notes d'un utilisateur."""
        ratings_to_delete = [
            r for r in self._ratings.values() if r.user_id == user_id
        ]
        for rating in ratings_to_delete:
            del self._ratings[rating.id]
        if user_id in self._user_ratings:
            # Mettre à jour l'index inverse
            for item_id in self._user_ratings[user_id]:
                if item_id in self._item_ratings:
                    self._item_ratings[item_id].pop(user_id, None)
            del self._user_ratings[user_id]