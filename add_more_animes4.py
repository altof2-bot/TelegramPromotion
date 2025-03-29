"""
Script pour ajouter encore plus d'animes à la base de données locale (4ème partie)
avec des animes très populaires comme Boruto
"""

import logging
import json
from anime_data import add_anime, load_animes

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def add_animes_to_database():
    """
    Ajoute de nouveaux animes à la base de données
    """
    # Liste des animes à ajouter
    animes_to_add = [
        {
            "titre": "Boruto: Naruto Next Generations",
            "titre_japonais": "ボルト: ナルト ネクスト ジェネレーションズ",
            "image": "https://cdn.myanimelist.net/images/anime/9/84460.jpg",
            "synopsis": "Suite de la série Naruto, Boruto suit les aventures du fils de Naruto Uzumaki, Boruto, qui entre à l'académie ninja et cherche à se faire un nom en dehors de l'ombre de son père.",
            "date_debut": "2017-04-05",
            "date_fin": "",
            "episodes": 293,
            "duree": "23 min par épisode",
            "status": "En cours",
            "score": 6.86,
            "genres": ["Action", "Aventure", "Arts Martiaux", "Shōnen"],
            "studios": ["Studio Pierrot"],
            "popularite": 20
        },
        {
            "titre": "Dragon Ball Super",
            "titre_japonais": "ドラゴンボール超スーパー",
            "image": "https://cdn.myanimelist.net/images/anime/7/74606.jpg",
            "synopsis": "Suite de Dragon Ball Z, l'histoire reprend après la défaite de Majin Buu, alors que la Terre connaît une période de paix. Cependant, de nouvelles menaces apparaissent, notamment des dieux de la destruction.",
            "date_debut": "2015-07-05",
            "date_fin": "2018-03-25",
            "episodes": 131,
            "duree": "24 min par épisode",
            "status": "Terminé",
            "score": 7.59,
            "genres": ["Action", "Aventure", "Comédie", "Arts Martiaux", "Fantastique", "Shōnen"],
            "studios": ["Toei Animation"],
            "popularite": 15
        },
        {
            "titre": "Chainsaw Man",
            "titre_japonais": "チェンソーマン",
            "image": "https://cdn.myanimelist.net/images/anime/1806/126216.jpg",
            "synopsis": "Denji est un adolescent qui vit dans la pauvreté, tentant de rembourser la dette laissée par son père en travaillant comme Devil Hunter avec son démon Pochita. Après avoir été trahi et tué, Denji fusionne avec Pochita et devient Chainsaw Man.",
            "date_debut": "2022-10-12",
            "date_fin": "2022-12-28",
            "episodes": 12,
            "duree": "24 min par épisode",
            "status": "Terminé",
            "score": 8.54,
            "genres": ["Action", "Fantastique", "Horreur", "Shōnen"],
            "studios": ["MAPPA"],
            "popularite": 5
        },
        {
            "titre": "Jujutsu Kaisen",
            "titre_japonais": "呪術廻戦",
            "image": "https://cdn.myanimelist.net/images/anime/1171/109222.jpg",
            "synopsis": "Yuji Itadori, un lycéen doté d'une force physique extraordinaire, rejoint un groupe secret de sorciers pour éliminer une puissante malédiction après avoir avalé un doigt maudit appartenant à Ryomen Sukuna.",
            "date_debut": "2020-10-03",
            "date_fin": "2021-03-27",
            "episodes": 24,
            "duree": "23 min par épisode",
            "status": "Terminé",
            "score": 8.71,
            "genres": ["Action", "Démons", "Surnaturel", "Fantastique", "Shōnen"],
            "studios": ["MAPPA"],
            "popularite": 4
        },
        {
            "titre": "Spy x Family",
            "titre_japonais": "スパイファミリー",
            "image": "https://cdn.myanimelist.net/images/anime/1441/122795.jpg",
            "synopsis": "Pour maintenir la paix entre deux nations rivales, un agent secret nommé Twilight doit former une famille fictive pour accomplir sa mission. Sans le savoir, il adopte une fille télépathe et épouse une tueuse à gages.",
            "date_debut": "2022-04-09",
            "date_fin": "2022-12-24",
            "episodes": 25,
            "duree": "24 min par épisode",
            "status": "Terminé",
            "score": 8.61,
            "genres": ["Action", "Comédie", "Espionnage", "Shōnen"],
            "studios": ["Wit Studio", "CloverWorks"],
            "popularite": 8
        },
        {
            "titre": "One Piece",
            "titre_japonais": "ワンピース",
            "image": "https://cdn.myanimelist.net/images/anime/6/73245.jpg",
            "synopsis": "Monkey D. Luffy s'embarque dans un voyage pour trouver le trésor légendaire, le One Piece, et devenir le Roi des Pirates. Il forme un équipage de pirates et affronte de nombreux adversaires.",
            "date_debut": "1999-10-20",
            "date_fin": "",
            "episodes": 1095,
            "duree": "24 min par épisode",
            "status": "En cours",
            "score": 8.69,
            "genres": ["Action", "Aventure", "Comédie", "Drame", "Fantastique", "Shōnen"],
            "studios": ["Toei Animation"],
            "popularite": 2
        },
        {
            "titre": "Naruto Shippuden",
            "titre_japonais": "ナルト 疾風伝",
            "image": "https://cdn.myanimelist.net/images/anime/5/17407.jpg",
            "synopsis": "Après 2 ans et demi d'entraînement, Naruto Uzumaki revient dans son village caché de Konoha, plus fort que jamais, prêt à affronter l'organisation criminelle Akatsuki et à retrouver son ami Sasuke.",
            "date_debut": "2007-02-15",
            "date_fin": "2017-03-23",
            "episodes": 500,
            "duree": "23 min par épisode",
            "status": "Terminé",
            "score": 8.25,
            "genres": ["Action", "Aventure", "Comédie", "Arts Martiaux", "Shōnen"],
            "studios": ["Studio Pierrot"],
            "popularite": 7
        },
        {
            "titre": "Bleach",
            "titre_japonais": "ブリーチ",
            "image": "https://cdn.myanimelist.net/images/anime/3/40451.jpg",
            "synopsis": "Ichigo Kurosaki, un adolescent capable de voir les fantômes, devient un Shinigami (Dieu de la Mort) après avoir reçu des pouvoirs d'une Shinigami blessée nommée Rukia Kuchiki.",
            "date_debut": "2004-10-05",
            "date_fin": "2012-03-27",
            "episodes": 366,
            "duree": "24 min par épisode",
            "status": "Terminé",
            "score": 7.92,
            "genres": ["Action", "Aventure", "Comédie", "Fantastique", "Shōnen"],
            "studios": ["Studio Pierrot"],
            "popularite": 18
        },
        {
            "titre": "Demon Slayer: Kimetsu no Yaiba",
            "titre_japonais": "鬼滅の刃",
            "image": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg",
            "synopsis": "Après que sa famille a été brutalement massacrée et que sa sœur a été transformée en démon, Tanjirou Kamado décide de devenir un tueur de démons pour venger sa famille et trouver un remède pour sa sœur.",
            "date_debut": "2019-04-06",
            "date_fin": "2019-09-28",
            "episodes": 26,
            "duree": "23 min par épisode",
            "status": "Terminé",
            "score": 8.53,
            "genres": ["Action", "Démons", "Historique", "Shōnen", "Surnaturel"],
            "studios": ["ufotable"],
            "popularite": 3
        },
        {
            "titre": "Attack on Titan",
            "titre_japonais": "進撃の巨人",
            "image": "https://cdn.myanimelist.net/images/anime/10/47347.jpg",
            "synopsis": "Dans un monde où l'humanité vit à l'intérieur de villes entourées d'énormes murs pour se protéger des Titans, des créatures gigantesques qui dévorent les humains, Eren Yeager jure de se venger après que les Titans ont attaqué sa ville et tué sa mère.",
            "date_debut": "2013-04-07",
            "date_fin": "2013-09-29",
            "episodes": 25,
            "duree": "24 min par épisode",
            "status": "Terminé",
            "score": 8.54,
            "genres": ["Action", "Drame", "Fantastique", "Mystère", "Shōnen"],
            "studios": ["Wit Studio"],
            "popularite": 1
        }
    ]

    # Compteurs pour les statistiques
    added_count = 0
    skipped_count = 0

    # Ajouter chaque anime à la base de données
    for anime in animes_to_add:
        success, message = add_anime(anime)
        if success:
            logger.info(f"Anime ajouté: {anime['titre']}")
            added_count += 1
        else:
            logger.warning(f"Anime ignoré: {anime['titre']} - {message}")
            skipped_count += 1

    # Afficher les statistiques
    animes = load_animes()
    logger.info(f"Base de données mise à jour avec succès: {added_count} animes ajoutés, {skipped_count} ignorés")
    print(f"Résultat: {added_count} animes ajoutés, {skipped_count} ignorés")
    print(f"Nombre total d'animes dans la base de données: {len(animes)}")
    return added_count, skipped_count

if __name__ == "__main__":
    add_animes_to_database()