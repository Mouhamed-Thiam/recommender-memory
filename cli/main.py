from services.recommender_service import RecommenderService
from models.user import User
from models.item import Item
from models.rating import Rating

def main():
    service = RecommenderService()

    # Générer des données de test si le système est vide
    if not service.user_repo.get_all():
        print("Génération des données de test...")
        generate_test_data(service)

    while True:
        print("\n" + "="*50)
        print("SYSTÈME DE RECOMMANDATION PAR FILTRAGE COLLABORATIF")
        print("="*50)
        print("1. Gestion des utilisateurs")
        print("2. Gestion des films")
        print("3. Gestion des notes")
        print("4. Recommandations pour un utilisateur")
        print("5. Afficher les statistiques")
        print("0. Quitter")
        choice = input("\nVotre choix: ")

        if choice == "1":
            manage_users(service)
        elif choice == "2":
            manage_items(service)
        elif choice == "3":
            manage_ratings(service)
        elif choice == "4":
            show_recommendations(service)
        elif choice == "5":
            show_statistics(service)
        elif choice == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def generate_test_data(service):
    """Génère des données de test pour démonstration."""
    # Créer des utilisateurs
    alice = service.user_repo.create(User(None, "Alice"))
    bob = service.user_repo.create(User(None, "Bob"))
    charlie = service.user_repo.create(User(None, "Charlie"))
    david = service.user_repo.create(User(None, "David"))
    emma = service.user_repo.create(User(None, "Emma"))

    # Créer des films
    inception = service.item_repo.create(Item(None, "Inception", "Sci-Fi"))
    matrix = service.item_repo.create(Item(None, "The Matrix", "Sci-Fi"))
    titanic = service.item_repo.create(Item(None, "Titanic", "Romance"))
    avatar = service.item_repo.create(Item(None, "Avatar", "Sci-Fi"))
    gladiator = service.item_repo.create(Item(None, "Gladiator", "Action"))
    pulp_fiction = service.item_repo.create(Item(None, "Pulp Fiction", "Crime"))

    # Ajouter des notes
    service.rating_repo.create(Rating(None, alice.id, inception.id, 5))
    service.rating_repo.create(Rating(None, alice.id, matrix.id, 4))
    service.rating_repo.create(Rating(None, alice.id, titanic.id, 2))
    service.rating_repo.create(Rating(None, alice.id, gladiator.id, 3))

    service.rating_repo.create(Rating(None, bob.id, inception.id, 4))
    service.rating_repo.create(Rating(None, bob.id, matrix.id, 5))
    service.rating_repo.create(Rating(None, bob.id, avatar.id, 4))

    service.rating_repo.create(Rating(None, charlie.id, inception.id, 5))
    service.rating_repo.create(Rating(None, charlie.id, matrix.id, 3))
    service.rating_repo.create(Rating(None, charlie.id, titanic.id, 4))
    service.rating_repo.create(Rating(None, charlie.id, avatar.id, 5))

    service.rating_repo.create(Rating(None, david.id, inception.id, 3))
    service.rating_repo.create(Rating(None, david.id, titanic.id, 5))
    service.rating_repo.create(Rating(None, david.id, pulp_fiction.id, 4))

    service.rating_repo.create(Rating(None, emma.id, matrix.id, 4))
    service.rating_repo.create(Rating(None, emma.id, avatar.id, 3))
    service.rating_repo.create(Rating(None, emma.id, pulp_fiction.id, 5))

    print("Données de test générées avec 5 utilisateurs et 6 films.")

def manage_users(service):
    """Sous-menu pour la gestion des utilisateurs."""
    while True:
        print("\n--- Gestion des utilisateurs ---")
        print("1. Lister les utilisateurs")
        print("2. Ajouter un utilisateur")
        print("3. Supprimer un utilisateur")
        print("0. Retour")
        choice = input("Choix: ")

        if choice == "1":
            users = service.user_repo.get_all()
            if not users:
                print("Aucun utilisateur.")
            else:
                print("\nListe des utilisateurs:")
                for user in users:
                    nb_notes = len(service.rating_repo.get_ratings_by_user(user.id))
                    print(f"  [{user.id}] {user.name} ({nb_notes} notes)")
        elif choice == "2":
            name = input("Nom de l'utilisateur: ")
            if name.strip():
                user = service.user_repo.create(User(None, name.strip()))
                print(f"Utilisateur '{user.name}' ajouté avec l'ID {user.id}.")
            else:
                print("Nom invalide.")
        elif choice == "3":
            try:
                user_id = int(input("ID de l'utilisateur à supprimer: "))
                # Supprimer d'abord les notes de l'utilisateur
                service.rating_repo.delete_by_user(user_id)
                if service.user_repo.delete(user_id):
                    print(f"Utilisateur {user_id} supprimé.")
                else:
                    print("Utilisateur non trouvé.")
            except ValueError:
                print("ID invalide.")
        elif choice == "0":
            break
        else:
            print("Choix invalide.")

def manage_items(service):
    """Sous-menu pour la gestion des films."""
    while True:
        print("\n--- Gestion des films ---")
        print("1. Lister les films")
        print("2. Ajouter un film")
        print("3. Supprimer un film")
        print("0. Retour")
        choice = input("Choix: ")

        if choice == "1":
            items = service.item_repo.get_all()
            if not items:
                print("Aucun film.")
            else:
                print("\nListe des films:")
                for item in items:
                    nb_notes = len(service.rating_repo.get_ratings_by_item(item.id))
                    avg_rating = "N/A"
                    if nb_notes > 0:
                        ratings = service.rating_repo.get_ratings_by_item(item.id)
                        avg = sum(ratings.values()) / nb_notes
                        avg_rating = f"{avg:.2f}"
                    print(f"  [{item.id}] {item.title} ({item.genre}) - {nb_notes} notes, moyenne: {avg_rating}")
        elif choice == "2":
            title = input("Titre du film: ")
            genre = input("Genre: ")
            if title.strip():
                item = service.item_repo.create(Item(None, title.strip(), genre.strip() or None))
                print(f"Film '{item.title}' ajouté avec l'ID {item.id}.")
            else:
                print("Titre invalide.")
        elif choice == "3":
            try:
                item_id = int(input("ID du film à supprimer: "))
                if service.item_repo.delete(item_id):
                    print(f"Film {item_id} supprimé.")
                else:
                    print("Film non trouvé.")
            except ValueError:
                print("ID invalide.")
        elif choice == "0":
            break
        else:
            print("Choix invalide.")

def manage_ratings(service):
    """Sous-menu pour la gestion des notes."""
    while True:
        print("\n--- Gestion des notes ---")
        print("1. Voir les notes d'un utilisateur")
        print("2. Ajouter/Modifier une note")
        print("3. Supprimer une note")
        print("0. Retour")
        choice = input("Choix: ")

        if choice == "1":
            try:
                user_id = int(input("ID de l'utilisateur: "))
                user = service.user_repo.get_by_id(user_id)
                if not user:
                    print("Utilisateur non trouvé.")
                    continue
                ratings = service.rating_repo.get_ratings_by_user(user_id)
                if not ratings:
                    print(f"{user.name} n'a noté aucun film.")
                else:
                    print(f"\nNotes de {user.name}:")
                    for item_id, rating in ratings.items():
                        item = service.item_repo.get_by_id(item_id)
                        if item:
                            print(f"  - {item.title}: {rating}/5")
            except ValueError:
                print("ID invalide.")
        elif choice == "2":
            try:
                user_id = int(input("ID de l'utilisateur: "))
                item_id = int(input("ID du film: "))
                rating_value = int(input("Note (1-5): "))
                if rating_value < 1 or rating_value > 5:
                    print("La note doit être entre 1 et 5.")
                    continue

                user = service.user_repo.get_by_id(user_id)
                item = service.item_repo.get_by_id(item_id)

                if not user:
                    print("Utilisateur non trouvé.")
                    continue
                if not item:
                    print("Film non trouvé.")
                    continue

                # Vérifier si l'utilisateur a déjà noté ce film
                existing = service.rating_repo.get_ratings_by_user(user_id)
                if item_id in existing:
                    print("Note déjà existante. Supprimez-la d'abord pour la modifier.")
                else:
                    rating = service.rating_repo.create(Rating(None, user_id, item_id, rating_value))
                    print(f"Note ajoutée: {user.name} a noté {item.title} {rating_value}/5")
            except ValueError:
                print("Entrée invalide.")
        elif choice == "3":
            try:
                user_id = int(input("ID de l'utilisateur: "))
                item_id = int(input("ID du film: "))
                # Suppression via une méthode dédiée (à ajouter dans le repository)
                ratings = service.rating_repo.get_ratings_by_user(user_id)
                if item_id not in ratings:
                    print("Note non trouvée.")
                else:
                    # Trouver et supprimer la note
                    for rid, rating in service.rating_repo._ratings.items():
                        if rating.user_id == user_id and rating.item_id == item_id:
                            del service.rating_repo._ratings[rid]
                            break
                    # Mettre à jour les index
                    if user_id in service.rating_repo._user_ratings:
                        service.rating_repo._user_ratings[user_id].pop(item_id, None)
                    if item_id in service.rating_repo._item_ratings:
                        service.rating_repo._item_ratings[item_id].pop(user_id, None)
                    print("Note supprimée.")
            except ValueError:
                print("ID invalide.")
        elif choice == "0":
            break
        else:
            print("Choix invalide.")

def show_recommendations(service):
    """Affiche les recommandations pour un utilisateur."""
    try:
        user_id = int(input("ID de l'utilisateur: "))
        user = service.user_repo.get_by_id(user_id)
        if not user:
            print("Utilisateur non trouvé.")
            return

        top_n = int(input("Nombre de recommandations (défaut 5): ") or "5")
        min_sim = float(input("Similarité minimale (défaut 0.2): ") or "0.2")
        min_common = int(input("Minimum d'items communs (défaut 2): ") or "2")

        recommendations = service.recommend_items(user_id, top_n, min_sim, min_common)

        if not recommendations:
            print("\nAucune recommandation disponible.")
            print("Causes possibles:")
            print("- Pas assez d'utilisateurs similaires")
            print("- L'utilisateur a déjà noté tous les films")
            print("- Pas de films non notés par les utilisateurs similaires")
            return

        print(f"\nRecommandations pour {user.name}:")
        print("-" * 50)
        for i, (item, score) in enumerate(recommendations, 1):
            print(f"{i}. {item.title} ({item.genre})")
            print(f"   Note prédite: {score:.2f}/5")
            # Afficher qui a influencé cette recommandation
            similar_users = service.get_similar_users(user_id, min_common)
            influences = []
            for other_id, sim in similar_users[:3]:
                other_ratings = service.rating_repo.get_ratings_by_user(other_id)
                if item.id in other_ratings:
                    other = service.user_repo.get_by_id(other_id)
                    influences.append(f"{other.name} ({other_ratings[item.id]}/5, sim={sim:.2f})")
            if influences:
                print(f"   Influencé par: {', '.join(influences)}")
            print()
    except ValueError:
        print("Entrée invalide.")

def show_statistics(service):
    """Affiche les statistiques du système."""
    print("\n=== STATISTIQUES ===")

    users = service.user_repo.get_all()
    items = service.item_repo.get_all()
    ratings = service.rating_repo.get_all()

    print(f"Nombre d'utilisateurs: {len(users)}")
    print(f"Nombre de films: {len(items)}")
    print(f"Nombre total de notes: {len(ratings)}")

    if ratings:
        avg_rating = sum(r.rating for r in ratings) / len(ratings)
        print(f"Note moyenne globale: {avg_rating:.2f}/5")

    # Utilisateurs les plus actifs
    if users:
        user_activity = []
        for user in users:
            nb_ratings = len(service.rating_repo.get_ratings_by_user(user.id))
            user_activity.append((user.name, nb_ratings))
        user_activity.sort(key=lambda x: x[1], reverse=True)
        print("\nTop 3 des utilisateurs les plus actifs:")
        for name, count in user_activity[:3]:
            print(f"  - {name}: {count} notes")

    # Films les mieux notés (avec au moins 2 notes)
    if items:
        item_ratings = []
        for item in items:
            ratings_dict = service.rating_repo.get_ratings_by_item(item.id)
            if len(ratings_dict) >= 2:
                avg = sum(ratings_dict.values()) / len(ratings_dict)
                item_ratings.append((item.title, avg, len(ratings_dict)))
        item_ratings.sort(key=lambda x: x[1], reverse=True)
        print("\nTop 3 des films les mieux notés (min 2 notes):")
        for title, avg, count in item_ratings[:3]:
            print(f"  - {title}: {avg:.2f}/5 ({count} notes)")

if __name__ == "__main__":
    main()