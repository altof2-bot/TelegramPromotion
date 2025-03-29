"""
Script pour ajouter de nouveaux animes à la base de données locale
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
        "titre": "Cowboy Bebop",
        "titre_japonais": "カウボーイビバップ",
        "image": "https://cdn.myanimelist.net/images/anime/4/19644.jpg",
        "synopsis": "Dans un futur où l'humanité a colonisé le système solaire, l'équipage du vaisseau Bebop, composé de chasseurs de primes, parcourt l'espace à la recherche de criminels. Chacun fuit un passé douloureux qui le rattrape inexorablement.",
        "date_debut": "1998-04-03",
        "date_fin": "1999-04-24",
        "episodes": 26,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.78,
        "genres": ["Action", "Aventure", "Drame", "Sci-Fi", "Espace"],
        "studios": ["Sunrise"],
        "popularite": 15
    },
    {
        "titre": "Code Geass",
        "titre_japonais": "コードギアス 反逆のルルーシュ",
        "image": "https://cdn.myanimelist.net/images/anime/5/50331.jpg",
        "synopsis": "Dans un monde dominé par l'Empire de Britannia, Lelouch, un prince exilé, obtient un pouvoir mystérieux appelé Geass qui lui permet de contrôler la volonté des autres. Il l'utilisera pour se venger et changer le monde.",
        "date_debut": "2006-10-06",
        "date_fin": "2007-07-28",
        "episodes": 25,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.70,
        "genres": ["Action", "Drame", "Mecha", "Militaire", "Sci-Fi", "Super Pouvoirs"],
        "studios": ["Sunrise"],
        "popularite": 12
    },
    {
        "titre": "Steins;Gate",
        "titre_japonais": "シュタインズ・ゲート",
        "image": "https://cdn.myanimelist.net/images/anime/5/73199.jpg",
        "synopsis": "Rintaro Okabe, un scientifique autoproclamé, et ses amis créent accidentellement un dispositif capable d'envoyer des messages dans le passé, modifiant ainsi le cours de l'histoire et provoquant des conséquences imprévues.",
        "date_debut": "2011-04-06",
        "date_fin": "2011-09-14",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 9.08,
        "genres": ["Drame", "Psychologique", "Sci-Fi", "Thriller"],
        "studios": ["White Fox"],
        "popularite": 11
    },
    {
        "titre": "Your Name",
        "titre_japonais": "君の名は。",
        "image": "https://cdn.myanimelist.net/images/anime/5/87048.jpg",
        "synopsis": "Mitsuha et Taki ne se connaissent pas, mais se retrouvent mystérieusement liés par des rêves dans lesquels ils échangent leurs corps. Ils tentent alors de se retrouver, malgré l'espace et le temps qui les séparent.",
        "date_debut": "2016-08-26",
        "date_fin": "2016-08-26",
        "episodes": 1,
        "duree": "107 minutes",
        "status": "Terminé",
        "score": 8.85,
        "genres": ["Drame", "Romance", "Surnaturel"],
        "studios": ["CoMix Wave Films"],
        "popularite": 13
    },
    {
        "titre": "One Punch Man",
        "titre_japonais": "ワンパンマン",
        "image": "https://cdn.myanimelist.net/images/anime/12/76049.jpg",
        "synopsis": "Saitama est un héros capable de vaincre n'importe quel ennemi d'un seul coup de poing. Frustré par le manque de défi, il cherche un adversaire digne de ce nom tout en combattant le mal avec l'Association des Héros.",
        "date_debut": "2015-10-05",
        "date_fin": "2015-12-21",
        "episodes": 12,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.52,
        "genres": ["Action", "Comédie", "Super Pouvoirs", "Surnaturel"],
        "studios": ["Madhouse"],
        "popularite": 20
    },
    {
        "titre": "Naruto Shippuden",
        "titre_japonais": "ナルト 疾風伝",
        "image": "https://cdn.myanimelist.net/images/anime/5/17407.jpg",
        "synopsis": "Deux ans et demi se sont écoulés depuis que Naruto a quitté Konoha pour s'entraîner. De retour au village, il poursuit son rêve de devenir Hokage tout en affrontant l'organisation criminelle Akatsuki.",
        "date_debut": "2007-02-15",
        "date_fin": "2017-03-23",
        "episodes": 500,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.24,
        "genres": ["Action", "Aventure", "Comédie", "Super Pouvoirs", "Arts Martiaux", "Shonen"],
        "studios": ["Studio Pierrot"],
        "popularite": 14
    },
    {
        "titre": "Violet Evergarden",
        "titre_japonais": "ヴァイオレット・エヴァーガーデン",
        "image": "https://cdn.myanimelist.net/images/anime/1795/95088.jpg",
        "synopsis": "Violet Evergarden, une ancienne soldate devenue poupée de souvenirs automatiques, voyage pour comprendre les derniers mots de son major : 'Je t'aime'. À travers son métier d'écrivain public, elle découvre les émotions humaines.",
        "date_debut": "2018-01-11",
        "date_fin": "2018-04-05",
        "episodes": 13,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.67,
        "genres": ["Drame", "Fantasy", "Tranche de vie"],
        "studios": ["Kyoto Animation"],
        "popularite": 16
    },
    {
        "titre": "Tokyo Ghoul",
        "titre_japonais": "東京喰種トーキョーグール",
        "image": "https://cdn.myanimelist.net/images/anime/5/64449.jpg",
        "synopsis": "Ken Kaneki, un étudiant ordinaire, devient mi-humain mi-goule après une rencontre fatidique. Déchiré entre deux mondes, il doit apprendre à vivre en tant que goule tout en conservant son humanité.",
        "date_debut": "2014-07-04",
        "date_fin": "2014-09-19",
        "episodes": 12,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 7.79,
        "genres": ["Action", "Drame", "Horreur", "Mystère", "Psychologique", "Surnaturel"],
        "studios": ["Studio Pierrot"],
        "popularite": 18
    },
    {
        "titre": "Sword Art Online",
        "titre_japonais": "ソードアート・オンライン",
        "image": "https://cdn.myanimelist.net/images/anime/11/39717.jpg",
        "synopsis": "En 2022, des joueurs se retrouvent piégés dans un MMORPG en réalité virtuelle. Pour en sortir, ils doivent terminer le jeu, mais la mort dans le jeu signifie la mort dans la réalité.",
        "date_debut": "2012-07-08",
        "date_fin": "2012-12-23",
        "episodes": 25,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 7.20,
        "genres": ["Action", "Aventure", "Fantasy", "Jeu", "Romance"],
        "studios": ["A-1 Pictures"],
        "popularite": 19
    },
    {
        "titre": "L'Attaque des Titans: Saison 2",
        "titre_japonais": "進撃の巨人 Season 2",
        "image": "https://cdn.myanimelist.net/images/anime/4/84177.jpg",
        "synopsis": "Eren et ses compagnons du Bataillon d'exploration continuent leur combat contre les Titans, mais découvrent bientôt que l'ennemi est plus proche qu'ils ne le pensaient.",
        "date_debut": "2017-04-01",
        "date_fin": "2017-06-17",
        "episodes": 12,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.51,
        "genres": ["Action", "Drame", "Fantasy", "Mystère", "Shonen"],
        "studios": ["Wit Studio"],
        "popularite": 17
    },
    {
        "titre": "Assassination Classroom",
        "titre_japonais": "暗殺教室",
        "image": "https://cdn.myanimelist.net/images/anime/5/75639.jpg",
        "synopsis": "Un étrange professeur à tête de smiley, capable de se déplacer à Mach 20, menace de détruire la Terre. Avant cela, il décide d'enseigner à une classe de lycéens rejetés, qui doivent tenter de l'assassiner avant la fin de l'année scolaire.",
        "date_debut": "2015-01-10",
        "date_fin": "2015-06-20",
        "episodes": 22,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.12,
        "genres": ["Action", "Comédie", "École", "Shonen"],
        "studios": ["Lerche"],
        "popularite": 21
    },
    {
        "titre": "Death Parade",
        "titre_japonais": "デス・パレード",
        "image": "https://cdn.myanimelist.net/images/anime/5/71553.jpg",
        "synopsis": "Dans un bar mystérieux nommé Quindecim, un arbitre jugera l'âme des personnes décédées à travers des jeux révélant leur vraie nature, avant de décider de leur destination finale.",
        "date_debut": "2015-01-10",
        "date_fin": "2015-03-28",
        "episodes": 12,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.18,
        "genres": ["Drame", "Mystère", "Psychologique", "Thriller"],
        "studios": ["Madhouse"],
        "popularite": 25
    },
    {
        "titre": "Made in Abyss",
        "titre_japonais": "メイドインアビス",
        "image": "https://cdn.myanimelist.net/images/anime/6/86733.jpg",
        "synopsis": "Riko, une jeune orpheline, rêve de devenir Siffleur comme sa mère et d'explorer l'Abysse, un gigantesque trou mystérieux. Accompagnée d'un étrange robot nommé Reg, elle entame une descente périlleuse dans les profondeurs.",
        "date_debut": "2017-07-07",
        "date_fin": "2017-09-29",
        "episodes": 13,
        "duree": "25 minutes par épisode",
        "status": "Terminé",
        "score": 8.66,
        "genres": ["Aventure", "Drame", "Fantasy", "Mystère", "Sci-Fi"],
        "studios": ["Kinema Citrus"],
        "popularite": 26
    },
    {
        "titre": "Demon Slayer: Le train de l'infini",
        "titre_japonais": "鬼滅の刃 無限列車編",
        "image": "https://cdn.myanimelist.net/images/anime/1704/106947.jpg",
        "synopsis": "Tanjiro et ses compagnons rejoignent Rengoku, le Pilier de la Flamme, pour affronter un démon qui a fait disparaître plus de quarante personnes à bord du train de l'infini.",
        "date_debut": "2020-10-16",
        "date_fin": "2020-10-16",
        "episodes": 1,
        "duree": "117 minutes",
        "status": "Terminé",
        "score": 8.76,
        "genres": ["Action", "Aventure", "Surnaturel", "Démons", "Historique"],
        "studios": ["ufotable"],
        "popularite": 28
    },
    {
        "titre": "Dr. Stone",
        "titre_japonais": "ドクターストーン",
        "image": "https://cdn.myanimelist.net/images/anime/1613/102576.jpg",
        "synopsis": "Après une mystérieuse catastrophe qui a pétrifié toute l'humanité, Senku, un génie scientifique, se réveille 3700 ans plus tard et entreprend de faire renaître la civilisation grâce à la science.",
        "date_debut": "2019-07-05",
        "date_fin": "2019-12-13",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.28,
        "genres": ["Aventure", "Comédie", "Sci-Fi", "Shonen"],
        "studios": ["TMS Entertainment"],
        "popularite": 30
    },
    {
        "titre": "Vinland Saga",
        "titre_japonais": "ヴィンランド・サガ",
        "image": "https://cdn.myanimelist.net/images/anime/1500/103005.jpg",
        "synopsis": "Au début du 11e siècle, le jeune Thorfinn rejoint les mercenaires qui ont tué son père pour se venger, mais la voie de la vengeance le mènera à une remise en question de ses valeurs et à la recherche d'un monde pacifique.",
        "date_debut": "2019-07-08",
        "date_fin": "2019-12-30",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.73,
        "genres": ["Action", "Aventure", "Drame", "Historique", "Seinen"],
        "studios": ["Wit Studio"],
        "popularite": 23
    },
    {
        "titre": "Mob Psycho 100",
        "titre_japonais": "モブサイコ100",
        "image": "https://cdn.myanimelist.net/images/anime/5/80084.jpg",
        "synopsis": "Shigeo Kageyama, surnommé Mob, est un collégien doté de puissants pouvoirs psychiques. Travaillant pour Reigen, un médium arnaqueur, il lutte pour contrôler ses émotions qui, à 100%, déclenchent ses pouvoirs de façon incontrôlable.",
        "date_debut": "2016-07-12",
        "date_fin": "2016-09-27",
        "episodes": 12,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.48,
        "genres": ["Action", "Comédie", "Surnaturel", "Super Pouvoirs"],
        "studios": ["Bones"],
        "popularite": 22
    },
    {
        "titre": "Haikyuu!!",
        "titre_japonais": "ハイキュー!!",
        "image": "https://cdn.myanimelist.net/images/anime/7/76014.jpg",
        "synopsis": "Hinata Shoyo rejoint l'équipe de volleyball du lycée Karasuno, déterminé à devenir le meilleur malgré sa petite taille. Son talent naturel et sa persévérance, combinés à la présence du génie passeur Kageyama, transforment l'équipe.",
        "date_debut": "2014-04-06",
        "date_fin": "2014-09-21",
        "episodes": 25,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.45,
        "genres": ["Comédie", "Drame", "Sports", "École", "Shonen"],
        "studios": ["Production I.G"],
        "popularite": 24
    },
    {
        "titre": "Re:Zero",
        "titre_japonais": "Re：ゼロから始める異世界生活",
        "image": "https://cdn.myanimelist.net/images/anime/11/79410.jpg",
        "synopsis": "Subaru Natsuki est soudainement transporté dans un monde fantastique. Il y découvre qu'il possède un pouvoir qui le ramène dans le temps à sa mort. Il luttera pour sauver ceux qui lui sont chers de destins tragiques.",
        "date_debut": "2016-04-04",
        "date_fin": "2016-09-19",
        "episodes": 25,
        "duree": "25 minutes par épisode",
        "status": "Terminé",
        "score": 8.24,
        "genres": ["Drame", "Fantasy", "Psychologique", "Thriller"],
        "studios": ["White Fox"],
        "popularite": 27
    },
    {
        "titre": "No Game No Life",
        "titre_japonais": "ノーゲーム・ノーライフ",
        "image": "https://cdn.myanimelist.net/images/anime/5/65187.jpg",
        "synopsis": "Sora et Shiro, deux gamers légendaires formant le duo 'Blank', sont transportés dans un monde où tout se règle par des jeux. Ils entreprennent de conquérir ce monde pour défier le dieu des jeux.",
        "date_debut": "2014-04-09",
        "date_fin": "2014-06-25",
        "episodes": 12,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.14,
        "genres": ["Aventure", "Comédie", "Ecchi", "Fantasy", "Jeu"],
        "studios": ["Madhouse"],
        "popularite": 29
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