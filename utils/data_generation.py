import pytest
from services.recommender_service import RecommenderService
from models.user import User
from models.item import Item
from models.rating import Rating

@pytest.fixture
def service():
    """Fixture qui crée un service avec des données de test."""
    svc = RecommenderService()

    # Créer des utilisateurs
    alice = svc.user_repo.create(User(None, "Alice"))
    bob = svc.user_repo.create(User(None, "Bob"))

    # Créer des films
    inception = svc.item_repo.create(Item(None, "Inception", "Sci-Fi"))
    matrix = svc.item_repo.create(Item(None, "The Matrix", "Sci-Fi"))

    # Ajouter des notes
    svc.rating_repo.create(Rating(None, alice.id, inception.id, 5))
    svc.rating_repo.create(Rating(None, alice.id, matrix.id, 4))
    svc.rating_repo.create(Rating(None, bob.id, inception.id, 5))
    svc.rating_repo.create(Rating(None, bob.id, matrix.id, 5))

    return svc, alice, bob, inception, matrix

def test_cosine_similarity(service):
    svc, alice, bob, _, _ = service
    alice_ratings = svc.rating_repo.get_ratings_by_user(alice.id)
    bob_ratings = svc.rating_repo.get_ratings_by_user(bob.id)
    similarity = svc.cosine_similarity(alice_ratings, bob_ratings)
    # Alice a 5,4 et Bob a 5,5 -> similarité proche de 0.99
    assert similarity > 0.98

def test_get_similar_users(service):
    svc, alice, bob, _, _ = service
    similar = svc.get_similar_users(alice.id, min_common=1)
    assert len(similar) == 1
    assert similar[0][0] == bob.id