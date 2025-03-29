"""
Base de données locale d'animes populaires pour la recherche
"""

import logging
import json
import os
from datetime import datetime
import re
import uuid

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Fichier de la base de données
DATABASE_FILE = 'animes_db.json'

# Données par défaut pour quelques animes populaires
DEFAULT_ANIMES = [
    {
        "id": 1,
        "titre": "Naruto",
        "titre_japonais": "ナルト",
        "image": "https://cdn.myanimelist.net/images/anime/13/17405.jpg",
        "synopsis": "Naruto Uzumaki, un jeune ninja hyperactif, rêve de devenir le Hokage de son village pour être reconnu par tous. Mais Naruto a un lourd secret : il est le réceptacle du démon Kyuubi qui a autrefois ravagé le village de Konoha.",
        "date_debut": "2002-10-03",
        "date_fin": "2007-02-08",
        "episodes": 220,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 7.98,
        "genres": ["Action", "Aventure", "Comédie", "Arts Martiaux", "Shonen"],
        "studios": ["Studio Pierrot"],
        "popularite": 5
    },
    {
        "id": 2,
        "titre": "One Piece",
        "titre_japonais": "ワンピース",
        "image": "https://cdn.myanimelist.net/images/anime/6/73245.jpg",
        "synopsis": "Gold Roger, le légendaire Roi des Pirates, avant de mourir, a révélé l'existence du 'One Piece', un fabuleux trésor. Monkey D. Luffy, un jeune garçon rêve de retrouver ce trésor légendaire et de devenir le nouveau Roi des Pirates.",
        "date_debut": "1999-10-20",
        "date_fin": "",
        "episodes": 1000,
        "duree": "24 minutes par épisode",
        "status": "En cours",
        "score": 8.54,
        "genres": ["Action", "Aventure", "Comédie", "Drame", "Fantaisie", "Shonen"],
        "studios": ["Toei Animation"],
        "popularite": 2
    },
    {
        "id": 3,
        "titre": "Attack on Titan",
        "titre_japonais": "進撃の巨人",
        "image": "https://cdn.myanimelist.net/images/anime/10/47347.jpg",
        "synopsis": "Dans un monde ravagé par des titans mangeurs d'homme, les survivants de l'humanité ont construit d'immenses murs pour se protéger. Mais lorsqu'un titan colossal apparaît et détruit le mur extérieur, l'humanité fait face à une terreur sans précédent.",
        "date_debut": "2013-04-07",
        "date_fin": "2023-11-04",
        "episodes": 88,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 9.16,
        "genres": ["Action", "Drame", "Fantaisie", "Mystère", "Shonen"],
        "studios": ["Wit Studio", "MAPPA"],
        "popularite": 3
    },
    {
        "id": 4,
        "titre": "Demon Slayer",
        "titre_japonais": "鬼滅の刃",
        "image": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg",
        "synopsis": "Dans un Japon de l'ère Taisho, Tanjiro Kamado est le premier enfant d'une famille de marchands de charbon. Après que sa famille soit massacrée par un démon et que sa sœur ait été transformée en créature démoniaque, il devient un tueur de démons pour venger sa famille et guérir sa sœur.",
        "date_debut": "2019-04-06",
        "date_fin": "",
        "episodes": 44,
        "duree": "23 minutes par épisode",
        "status": "En cours",
        "score": 8.92,
        "genres": ["Action", "Aventure", "Surnaturel", "Démons", "Historique"],
        "studios": ["ufotable"],
        "popularite": 4
    },
    {
        "id": 5,
        "titre": "My Hero Academia",
        "titre_japonais": "僕のヒーローアカデミア",
        "image": "https://cdn.myanimelist.net/images/anime/10/78745.jpg",
        "synopsis": "Dans un monde où 80% de la population possède des super-pouvoirs appelés 'Alters', Izuku Midoriya a toujours rêvé d'être un héros. Malheureusement, il fait partie des 20% n'ayant aucun pouvoir, jusqu'à sa rencontre avec All Might, le plus grand des héros.",
        "date_debut": "2016-04-03",
        "date_fin": "",
        "episodes": 113,
        "duree": "23 minutes par épisode",
        "status": "En cours",
        "score": 8.23,
        "genres": ["Action", "Comédie", "Super Pouvoirs", "École", "Shonen"],
        "studios": ["Bones"],
        "popularite": 7
    },
    {
        "id": 6,
        "titre": "Dragon Ball Z",
        "titre_japonais": "ドラゴンボールZ",
        "image": "https://cdn.myanimelist.net/images/anime/1607/117271.jpg",
        "synopsis": "Cinq ans après avoir remporté le championnat du monde d'arts martiaux, Son Goku vit paisiblement avec sa femme et son fils. Mais tout bascule lorsque Raditz, un guerrier extraterrestre qui prétend être son frère, arrive sur Terre avec de sombres intentions.",
        "date_debut": "1989-04-26",
        "date_fin": "1996-01-31",
        "episodes": 291,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.16,
        "genres": ["Action", "Aventure", "Comédie", "Super Pouvoirs", "Arts Martiaux", "Shonen"],
        "studios": ["Toei Animation"],
        "popularite": 1
    },
    {
        "id": 7,
        "titre": "Death Note",
        "titre_japonais": "デスノート",
        "image": "https://cdn.myanimelist.net/images/anime/9/9453.jpg",
        "synopsis": "Light Yagami est un lycéen surdoué lassé par le monde corrompu qui l'entoure. Sa vie change radicalement le jour où il trouve le Death Note, un carnet donnant à son possesseur le pouvoir de tuer quiconque dont il connaît le nom et le visage.",
        "date_debut": "2006-10-04",
        "date_fin": "2007-06-27",
        "episodes": 37,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.62,
        "genres": ["Mystère", "Policier", "Psychologique", "Surnaturel", "Thriller"],
        "studios": ["Madhouse"],
        "popularite": 6
    },
    {
        "id": 8,
        "titre": "Fullmetal Alchemist: Brotherhood",
        "titre_japonais": "鋼の錬金術師 FULLMETAL ALCHEMIST",
        "image": "https://cdn.myanimelist.net/images/anime/1223/96541.jpg",
        "synopsis": "Après avoir perdu leur mère, les frères Elric tentent de la ressusciter grâce à l'alchimie, mais l'opération tourne mal. Edward perd un bras et une jambe, et Alphonse perd son corps entier. Ils partent alors à la recherche de la Pierre Philosophale pour retrouver leurs corps.",
        "date_debut": "2009-04-05",
        "date_fin": "2010-07-04",
        "episodes": 64,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 9.11,
        "genres": ["Action", "Aventure", "Drame", "Fantaisie", "Militaire", "Shonen"],
        "studios": ["Bones"],
        "popularite": 8
    },
    {
        "id": 9,
        "titre": "Hunter x Hunter (2011)",
        "titre_japonais": "ハンター×ハンター",
        "image": "https://cdn.myanimelist.net/images/anime/11/33657.jpg",
        "synopsis": "Gon Freecss découvre un jour que son père, qu'il croyait mort, est en fait un Hunter d'élite, un membre privilegié de la société. Décidé à suivre les traces de son père, Gon passe l'examen rigoureux de Hunter pour le retrouver.",
        "date_debut": "2011-10-02",
        "date_fin": "2014-09-24",
        "episodes": 148,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 9.05,
        "genres": ["Action", "Aventure", "Fantaisie", "Shonen"],
        "studios": ["Madhouse"],
        "popularite": 10
    },
    {
        "id": 10,
        "titre": "Jujutsu Kaisen",
        "titre_japonais": "呪術廻戦",
        "image": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg",
        "synopsis": "Yūji Itadori, un lycéen aux capacités physiques exceptionnelles, rejoint le club de spiritisme pour éviter l'athlétisme. Sa vie bascule lorsque de vrais esprits apparaissent à son école et qu'il avale un doigt maudit pour protéger ses amis, devenant ainsi l'hôte d'une malédiction nommée Ryomen Sukuna.",
        "date_debut": "2020-10-03",
        "date_fin": "",
        "episodes": 24,
        "duree": "23 minutes par épisode",
        "status": "En cours",
        "score": 8.78,
        "genres": ["Action", "Démons", "Surnaturel", "École", "Shonen"],
        "studios": ["MAPPA"],
        "popularite": 9
    }
]

def init_database():
    """
    Initialise la base de données avec les données par défaut si elle n'existe pas
    """
    if not os.path.exists(DATABASE_FILE):
        try:
            with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_ANIMES, f, ensure_ascii=False, indent=4)
            logger.info(f"Base de données initialisée avec {len(DEFAULT_ANIMES)} animes")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")

def save_animes(animes):
    """
    Sauvegarde la liste des animes dans la base de données
    
    Args:
        animes (list): Liste des animes à sauvegarder
    
    Returns:
        bool: True si la sauvegarde a réussi, False sinon
    """
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(animes, f, ensure_ascii=False, indent=4)
        logger.info(f"Base de données mise à jour avec {len(animes)} animes")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de la base de données: {e}")
        return False

def add_anime(anime_data):
    """
    Ajoute un nouvel anime à la base de données
    
    Args:
        anime_data (dict): Données de l'anime à ajouter
        
    Returns:
        tuple: (bool, str) - (Succès, Message)
    """
    # Charger la base de données actuelle
    animes = load_animes()
    
    # Vérifier que toutes les clés requises sont présentes
    required_keys = ['titre', 'titre_japonais', 'image', 'synopsis', 'date_debut', 
                     'episodes', 'duree', 'status', 'score', 'genres', 'studios']
    
    for key in required_keys:
        if key not in anime_data:
            return False, f"Champ requis manquant: {key}"
    
    # Générer un ID unique si non fourni
    if 'id' not in anime_data:
        # Trouver le plus grand ID existant et incrémenter
        max_id = max([anime.get('id', 0) for anime in animes], default=0)
        anime_data['id'] = max_id + 1
    
    # Vérifier si un anime avec ce titre existe déjà
    for anime in animes:
        if anime['titre'].lower() == anime_data['titre'].lower():
            return False, f"Un anime avec le titre '{anime_data['titre']}' existe déjà"
    
    # Vérifier si popularité est fournie, sinon lui attribuer une valeur par défaut
    if 'popularite' not in anime_data:
        anime_data['popularite'] = len(animes) + 1
    
    # Ajouter l'anime à la base de données
    animes.append(anime_data)
    
    # Sauvegarder la base de données
    if save_animes(animes):
        return True, f"Anime '{anime_data['titre']}' ajouté avec succès"
    else:
        return False, "Erreur lors de la sauvegarde de la base de données"

def delete_anime(anime_id):
    """
    Supprime un anime de la base de données par son ID
    
    Args:
        anime_id (int): ID de l'anime à supprimer
        
    Returns:
        tuple: (bool, str) - (Succès, Message)
    """
    # Charger la base de données actuelle
    animes = load_animes()
    
    # Convertir en entier si nécessaire
    if isinstance(anime_id, str):
        try:
            anime_id = int(anime_id)
        except ValueError:
            return False, f"ID d'anime invalide: {anime_id}"
    
    # Trouver l'anime à supprimer
    anime_to_delete = None
    for anime in animes:
        if anime.get('id') == anime_id:
            anime_to_delete = anime
            break
    
    if not anime_to_delete:
        return False, f"Aucun anime trouvé avec l'ID {anime_id}"
    
    # Supprimer l'anime
    animes.remove(anime_to_delete)
    
    # Sauvegarder la base de données
    if save_animes(animes):
        return True, f"Anime '{anime_to_delete['titre']}' supprimé avec succès"
    else:
        return False, "Erreur lors de la sauvegarde de la base de données"
    
def load_animes():
    """
    Charge la base de données des animes
    
    Returns:
        list: Liste des animes
    """
    init_database()
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la base de données: {e}")
        return DEFAULT_ANIMES

def search_anime(query, limit=5):
    """
    Recherche un anime par nom dans la base de données locale
    
    Args:
        query (str): Le nom de l'anime à rechercher
        limit (int): Nombre maximum de résultats
        
    Returns:
        list: Liste des animes correspondants à la recherche
    """
    animes = load_animes()
    
    # Si la requête est vide, retourner les animes les plus populaires
    if not query or query.strip() == "":
        # Trier par popularité et retourner les plus populaires
        popular_animes = sorted(animes, key=lambda x: x.get('popularite', 999), reverse=False)
        return popular_animes[:limit]
    
    # Convertir la requête en minuscules pour une recherche insensible à la casse
    query = query.lower().strip()
    
    # Préparer les résultats avec des scores pour trier par pertinence
    scored_results = []
    
    # 1. Recherche des correspondances exactes (titre complet)
    for anime in animes:
        titre_lower = anime['titre'].lower()
        titre_japonais_lower = anime.get('titre_japonais', '').lower()
        
        # Correspondance exacte avec le titre principal (score très élevé)
        if titre_lower == query:
            scored_results.append((anime, 100))
            continue
            
        # Correspondance exacte avec le titre japonais (score élevé)
        if titre_japonais_lower == query:
            scored_results.append((anime, 90))
            continue
    
    # 2. Recherche des titres qui commencent par la requête (score élevé)
    for anime in animes:
        if anime in [r[0] for r in scored_results]:
            continue  # Éviter les doublons
            
        titre_lower = anime['titre'].lower()
        titre_japonais_lower = anime.get('titre_japonais', '').lower()
        
        if titre_lower.startswith(query):
            scored_results.append((anime, 80))
            continue
            
        if titre_japonais_lower.startswith(query):
            scored_results.append((anime, 70))
            continue
    
    # 3. Recherche pour les titres qui contiennent la requête comme sous-chaîne (score moyen)
    for anime in animes:
        if anime in [r[0] for r in scored_results]:
            continue  # Éviter les doublons
            
        titre_lower = anime['titre'].lower()
        titre_japonais_lower = anime.get('titre_japonais', '').lower()
        
        if query in titre_lower:
            # Calculer un score basé sur la position (plus c'est au début, mieux c'est)
            position_score = 60 - (titre_lower.find(query) / len(titre_lower)) * 20
            scored_results.append((anime, position_score))
            continue
            
        if query in titre_japonais_lower:
            position_score = 50 - (titre_japonais_lower.find(query) / len(titre_japonais_lower)) * 20
            scored_results.append((anime, position_score))
            continue
    
    # 4. Recherche par mots-clés (pour les requêtes multi-mots) avec score pondéré
    if len(query.split()) > 1 and len(scored_results) < limit:
        keywords = query.split()
        
        for anime in animes:
            if anime in [r[0] for r in scored_results]:
                continue  # Éviter les doublons
                
            titre_lower = anime['titre'].lower()
            titre_japonais_lower = anime.get('titre_japonais', '').lower()
            genres_lower = [g.lower() for g in anime.get('genres', [])]
            
            # Vérifier combien de mots-clés correspondent au titre ou aux genres
            match_count_title = sum(1 for keyword in keywords if keyword in titre_lower)
            match_count_japanese = sum(1 for keyword in keywords if keyword in titre_japonais_lower)
            match_count_genre = sum(1 for keyword in keywords if any(keyword in genre for genre in genres_lower))
            
            # Calculer un score composite
            total_matches = match_count_title + match_count_japanese + (match_count_genre * 0.5)
            keyword_ratio = total_matches / len(keywords)
            
            if keyword_ratio > 0:
                base_score = 40 * keyword_ratio
                scored_results.append((anime, base_score))
    
    # 5. Recherche dans les genres si peu de résultats
    if len(scored_results) < limit:
        for anime in animes:
            if anime in [r[0] for r in scored_results]:
                continue  # Éviter les doublons
                
            genres_lower = [g.lower() for g in anime.get('genres', [])]
            
            # Si la requête correspond exactement à un genre
            if query in genres_lower:
                scored_results.append((anime, 35))
                continue
                
            # Si la requête est contenue dans un genre
            for genre in genres_lower:
                if query in genre:
                    scored_results.append((anime, 30))
                    break
    
    # Trier par score de pertinence (du plus élevé au plus bas)
    scored_results.sort(key=lambda x: x[1], reverse=True)
    
    # Ne garder que les animes jusqu'à la limite demandée
    results = [anime for anime, score in scored_results[:limit]]
    
    # Si aucun résultat n'a été trouvé avec les méthodes précédentes, on utilise 
    # un dernier recours avec une recherche plus souple
    if not results and limit > 0:
        # Utiliser une recherche approximative (rechercher chaque caractère séparément)
        char_matches = {}
        for anime in animes:
            titre_lower = anime['titre'].lower()
            match_count = 0
            for char in query:
                if char in titre_lower:
                    match_count += 1
            
            # Au moins la moitié des caractères doivent correspondre
            if match_count >= len(query) / 2:
                char_ratio = match_count / len(query)
                scored_results.append((anime, 25 * char_ratio))
        
        # Trier et limiter les résultats
        scored_results.sort(key=lambda x: x[1], reverse=True)
        results = [anime for anime, score in scored_results[:limit]]
        
        # Si toujours rien, retourner simplement les animes les plus populaires
        if not results:
            popular_animes = sorted(animes, key=lambda x: x.get('popularite', 999), reverse=False)
            return popular_animes[:limit]
    
    return results

def format_date(date_str):
    """
    Formate une date pour l'affichage
    
    Args:
        date_str (str): Date au format ISO
        
    Returns:
        str: Date formatée
    """
    if not date_str:
        return "?"
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%d/%m/%Y")
    except ValueError:
        return date_str

def format_anime_message(anime):
    """
    Formate les informations d'un anime pour l'affichage dans Telegram
    
    Args:
        anime (dict): Les données de l'anime
        
    Returns:
        str: Message formaté pour Telegram
    """
    try:
        # Informations de base
        message = f"<b>📺 {anime['titre']}</b>\n"
        message += f"<b>🇯🇵 Titre japonais:</b> {anime['titre_japonais']}\n\n"
        
        # Score et popularité
        message += f"<b>⭐ Score:</b> {anime['score']} | <b>👥 Popularité:</b> #{anime['popularite']}\n"
        
        # Statut et dates
        status = anime['status']
        date_debut = format_date(anime['date_debut'])
        date_fin = format_date(anime['date_fin']) if anime['date_fin'] else "En cours"
        
        message += f"<b>📆 Diffusion:</b> {date_debut} → {date_fin}\n"
        
        # Épisodes et durée
        episodes = anime['episodes']
        duree = anime['duree']
        message += f"<b>🎬 Épisodes:</b> {episodes} | <b>⏱ Durée:</b> {duree}\n"
        
        # Genres
        if anime['genres']:
            message += f"<b>🏷️ Genres:</b> {', '.join(anime['genres'])}\n"
            
        # Studios
        if anime['studios']:
            message += f"<b>🎨 Studios:</b> {', '.join(anime['studios'])}\n"
            
        # Synopsis
        synopsis = anime['synopsis']
        if len(synopsis) > 300:
            synopsis = synopsis[:297] + "..."
        message += f"\n<b>📝 Synopsis:</b>\n{synopsis}\n"
            
        return message
    except Exception as e:
        logger.error(f"Erreur lors du formatage du message: {e}")
        return "Erreur lors du formatage des informations de l'anime."