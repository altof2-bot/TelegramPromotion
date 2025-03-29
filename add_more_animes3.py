"""
Script pour ajouter encore plus d'animes à la base de données locale (3ème partie)
"""

import json
import os
from datetime import datetime
import logging
from anime_data import load_animes, save_animes

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Liste des animes supplémentaires à ajouter
NEW_ANIMES = [
    {
        "titre": "Clannad: After Story",
        "titre_japonais": "クラナド アフターストーリー",
        "image": "https://cdn.myanimelist.net/images/anime/1299/110774.jpg",
        "synopsis": "Suite de Clannad, cette série suit Tomoya et Nagisa dans leur vie d'adultes. Lorsque la tragédie frappe, Tomoya doit apprendre à faire face à ses responsabilités et à trouver un sens à sa vie.",
        "date_debut": "2008-10-03",
        "date_fin": "2009-03-27",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.94,
        "genres": ["Drame", "Romance", "Surnaturel", "Tranche de vie"],
        "studios": ["Kyoto Animation"],
        "popularite": 52
    },
    {
        "titre": "Violet Evergarden: The Movie",
        "titre_japonais": "劇場版 ヴァイオレット・エヴァーガーデン",
        "image": "https://cdn.myanimelist.net/images/anime/1825/110716.jpg",
        "synopsis": "Plusieurs années après la fin de la guerre, Violet Evergarden continue d'aider les gens à exprimer leurs sentiments à travers ses lettres, tout en cherchant à comprendre ses propres émotions et à découvrir ce qui est arrivé au Major Gilbert.",
        "date_debut": "2020-09-18",
        "date_fin": "2020-09-18",
        "episodes": 1,
        "duree": "140 minutes",
        "status": "Terminé",
        "score": 8.91,
        "genres": ["Drame", "Fantasy", "Tranche de vie"],
        "studios": ["Kyoto Animation"],
        "popularite": 53
    },
    {
        "titre": "Demon Slayer: Entertainment District Arc",
        "titre_japonais": "鬼滅の刃 遊郭編",
        "image": "https://cdn.myanimelist.net/images/anime/1908/120036.jpg",
        "synopsis": "Tanjiro, Zenitsu et Inosuke, accompagnés par Nezuko et le Pilier du Son Tengen Uzui, se rendent dans le quartier des plaisirs pour traquer un démon qui se cache parmi les courtisanes.",
        "date_debut": "2021-12-05",
        "date_fin": "2022-02-13",
        "episodes": 11,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.86,
        "genres": ["Action", "Aventure", "Démons", "Historique", "Shonen", "Surnaturel"],
        "studios": ["ufotable"],
        "popularite": 54
    },
    {
        "titre": "Samurai Champloo",
        "titre_japonais": "サムライチャンプルー",
        "image": "https://cdn.myanimelist.net/images/anime/1375/121599.jpg",
        "synopsis": "Dans un Japon alternatif de l'ère Edo, Fuu, une serveuse, sauve deux samouraïs aux styles de combat opposés, Mugen et Jin. Elle les engage pour l'aider à trouver 'le samouraï qui sent le tournesol', entamant un voyage rempli d'aventures.",
        "date_debut": "2004-05-20",
        "date_fin": "2005-03-19",
        "episodes": 26,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.48,
        "genres": ["Action", "Aventure", "Comédie", "Samouraï"],
        "studios": ["Manglobe"],
        "popularite": 55
    },
    {
        "titre": "Overlord",
        "titre_japonais": "オーバーロード",
        "image": "https://cdn.myanimelist.net/images/anime/7/88019.jpg",
        "synopsis": "Lorsque le jeu YGGDRASIL ferme ses serveurs, un joueur, Momonga, décide de rester jusqu'à la fin. Contre toute attente, il se retrouve piégé dans le jeu sous la forme de son personnage squelettique, et le monde virtuel prend vie autour de lui.",
        "date_debut": "2015-07-07",
        "date_fin": "2015-09-29",
        "episodes": 13,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 7.91,
        "genres": ["Action", "Aventure", "Fantasy", "Jeu", "Surnaturel"],
        "studios": ["Madhouse"],
        "popularite": 56
    },
    {
        "titre": "Kill la Kill",
        "titre_japonais": "キルラキル",
        "image": "https://cdn.myanimelist.net/images/anime/8/75514.jpg",
        "synopsis": "Ryuko Matoi arrive à l'Académie Honnouji avec une moitié de paire de ciseaux géants, à la recherche du meurtrier de son père. Elle défie la présidente du conseil des élèves, Satsuki Kiryuin, et découvre le pouvoir d'un uniforme vivant.",
        "date_debut": "2013-10-04",
        "date_fin": "2014-03-28",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.14,
        "genres": ["Action", "Comédie", "Ecchi", "Super Pouvoirs"],
        "studios": ["Trigger"],
        "popularite": 57
    },
    {
        "titre": "Tokyo Revengers",
        "titre_japonais": "東京リベンジャーズ",
        "image": "https://cdn.myanimelist.net/images/anime/1839/122012.jpg",
        "synopsis": "Takemichi Hanagaki apprend que son ex-petite amie a été tuée par un gang. Après un accident, il remonte 12 ans dans le passé et a la possibilité de changer le cours des événements pour sauver son ex-petite amie.",
        "date_debut": "2021-04-11",
        "date_fin": "2021-09-19",
        "episodes": 24,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.25,
        "genres": ["Action", "Drame", "Shonen", "Surnaturel"],
        "studios": ["LIDENFILMS"],
        "popularite": 58
    },
    {
        "titre": "Akame ga Kill!",
        "titre_japonais": "アカメが斬る!",
        "image": "https://cdn.myanimelist.net/images/anime/1429/95946.jpg",
        "synopsis": "Tatsumi part pour la capitale afin de gagner de l'argent pour son village. Il découvre la corruption qui y règne et rejoint Night Raid, un groupe d'assassins déterminés à renverser l'Empire corrompu.",
        "date_debut": "2014-07-07",
        "date_fin": "2014-12-15",
        "episodes": 24,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 7.47,
        "genres": ["Action", "Aventure", "Drame", "Fantasy", "Shonen"],
        "studios": ["White Fox"],
        "popularite": 59
    },
    {
        "titre": "Blue Exorcist",
        "titre_japonais": "青の祓魔師",
        "image": "https://cdn.myanimelist.net/images/anime/10/75195.jpg",
        "synopsis": "Rin Okumura découvre qu'il est le fils de Satan. Déterminé à le vaincre, il s'inscrit à l'Académie de la Croix-Vraie pour devenir exorciste, tout en cachant sa véritable nature aux autres.",
        "date_debut": "2011-04-17",
        "date_fin": "2011-10-02",
        "episodes": 25,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 7.49,
        "genres": ["Action", "Démons", "Fantasy", "Shonen", "Surnaturel"],
        "studios": ["A-1 Pictures"],
        "popularite": 60
    },
    {
        "titre": "Hellsing Ultimate",
        "titre_japonais": "ヘルシング アルティメット",
        "image": "https://cdn.myanimelist.net/images/anime/6/7333.jpg",
        "synopsis": "L'Organisation Hellsing protège l'Angleterre des vampires et autres forces surnaturelles. Leur arme ultime, Alucard, un vampire ancien et puissant, combat les ennemis alors qu'une guerre secrète se prépare.",
        "date_debut": "2006-02-10",
        "date_fin": "2012-12-26",
        "episodes": 10,
        "duree": "50 minutes par épisode",
        "status": "Terminé",
        "score": 8.36,
        "genres": ["Action", "Horreur", "Militaire", "Seinen", "Surnaturel", "Vampire"],
        "studios": ["Madhouse", "Satelight"],
        "popularite": 61
    }
]

def add_animes_to_database():
    """
    Ajoute de nouveaux animes à la base de données
    """
    # Charger les animes existants
    animes = load_animes()
    existing_ids = [anime['id'] for anime in animes]
    existing_titles = [anime['titre'].lower() for anime in animes]
    
    # Déterminer le prochain ID disponible
    next_id = max(existing_ids) + 1 if existing_ids else 1
    
    # Ajouter les nouveaux animes
    added_count = 0
    skipped_count = 0
    
    for anime in NEW_ANIMES:
        # Vérifier si l'anime existe déjà (par titre)
        if anime['titre'].lower() in existing_titles:
            logger.info(f"Anime déjà existant, ignoré: {anime['titre']}")
            skipped_count += 1
            continue
        
        # Assigner un ID si non présent
        if 'id' not in anime:
            anime['id'] = next_id
            next_id += 1
        
        # Ajouter l'anime à la liste
        animes.append(anime)
        added_count += 1
        logger.info(f"Anime ajouté: {anime['titre']}")
    
    # Sauvegarder la base de données mise à jour
    if added_count > 0:
        if save_animes(animes):
            logger.info(f"Base de données mise à jour avec succès: {added_count} animes ajoutés, {skipped_count} ignorés")
            return True, f"{added_count} animes ajoutés, {skipped_count} ignorés"
        else:
            logger.error("Erreur lors de la sauvegarde de la base de données")
            return False, "Erreur lors de la sauvegarde"
    else:
        logger.info(f"Aucun nouvel anime ajouté, {skipped_count} ignorés (déjà existants)")
        return True, f"Aucun nouvel anime ajouté, {skipped_count} ignorés"

if __name__ == "__main__":
    # Exécuter directement le script pour ajouter les animes
    success, message = add_animes_to_database()
    print(f"Résultat: {message}")
    
    # Afficher le nombre total d'animes
    animes = load_animes()
    print(f"Nombre total d'animes dans la base de données: {len(animes)}")