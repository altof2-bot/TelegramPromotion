"""
Script pour ajouter encore plus d'animes à la base de données locale
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
        "titre": "JoJo's Bizarre Adventure",
        "titre_japonais": "ジョジョの奇妙な冒険",
        "image": "https://cdn.myanimelist.net/images/anime/3/40409.jpg",
        "synopsis": "Des générations de la famille Joestar luttent contre des forces surnaturelles en utilisant des pouvoirs extraordinaires. Chaque partie suit un nouveau JoJo dans une aventure qui traverse différentes époques.",
        "date_debut": "2012-10-06",
        "date_fin": "2013-04-06",
        "episodes": 26,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.10,
        "genres": ["Action", "Aventure", "Surnaturel", "Vampire", "Shonen"],
        "studios": ["David Production"],
        "popularite": 31
    },
    {
        "titre": "Fate/Zero",
        "titre_japonais": "フェイト/ゼロ",
        "image": "https://cdn.myanimelist.net/images/anime/2/73249.jpg",
        "synopsis": "Sept mages et leurs serviteurs historiques s'affrontent dans la 4e Guerre du Saint Graal, un combat à mort pour obtenir le pouvoir de réaliser n'importe quel souhait.",
        "date_debut": "2011-10-02",
        "date_fin": "2011-12-25",
        "episodes": 13,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.32,
        "genres": ["Action", "Fantasy", "Surnaturel"],
        "studios": ["ufotable"],
        "popularite": 35
    },
    {
        "titre": "Your Lie in April",
        "titre_japonais": "四月は君の嘘",
        "image": "https://cdn.myanimelist.net/images/anime/3/67177.jpg",
        "synopsis": "Kosei Arima, un prodige du piano traumatisé, ne peut plus entendre les notes qu'il joue. Sa vie change lorsqu'il rencontre Kaori Miyazono, une violoniste passionnée qui l'aide à redécouvrir la musique.",
        "date_debut": "2014-10-10",
        "date_fin": "2015-03-20",
        "episodes": 22,
        "duree": "22 minutes par épisode",
        "status": "Terminé",
        "score": 8.67,
        "genres": ["Drame", "Musique", "Romance", "École", "Shonen"],
        "studios": ["A-1 Pictures"],
        "popularite": 32
    },
    {
        "titre": "Mushishi",
        "titre_japonais": "蟲師",
        "image": "https://cdn.myanimelist.net/images/anime/2/73862.jpg",
        "synopsis": "Ginko, un mushishi, voyage à travers le Japon rural pour étudier les mushi, des créatures primitives qui existent à la limite entre la vie et la mort, et aider ceux qui sont affectés par eux.",
        "date_debut": "2005-10-23",
        "date_fin": "2006-06-19",
        "episodes": 26,
        "duree": "25 minutes par épisode",
        "status": "Terminé",
        "score": 8.68,
        "genres": ["Aventure", "Fantastique", "Historique", "Mystère", "Seinen", "Slice of Life", "Surnaturel"],
        "studios": ["Artland"],
        "popularite": 50
    },
    {
        "titre": "Gintama",
        "titre_japonais": "銀魂",
        "image": "https://cdn.myanimelist.net/images/anime/10/73274.jpg",
        "synopsis": "Dans un Japon féodal envahi par des extraterrestres, le samouraï Gintoki Sakata travaille comme homme à tout faire avec ses amis pour payer son loyer, enchaînant les situations absurdes.",
        "date_debut": "2006-04-04",
        "date_fin": "2010-03-25",
        "episodes": 201,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.95,
        "genres": ["Action", "Comédie", "Science-fiction", "Parodie", "Samouraï", "Shonen"],
        "studios": ["Sunrise"],
        "popularite": 38
    },
    {
        "titre": "Kimetsu no Yaiba",
        "titre_japonais": "鬼滅の刃",
        "image": "https://cdn.myanimelist.net/images/anime/1286/99889.jpg",
        "synopsis": "Après le massacre de sa famille par un démon, Tanjiro devient un pourfendeur de démons pour venger sa famille et guérir sa sœur Nezuko, transformée en démon mais ayant gardé sa conscience humaine.",
        "date_debut": "2019-04-06",
        "date_fin": "2019-09-28",
        "episodes": 26,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.54,
        "genres": ["Action", "Démons", "Historique", "Shonen", "Surnaturel"],
        "studios": ["ufotable"],
        "popularite": 34
    },
    {
        "titre": "Black Clover",
        "titre_japonais": "ブラッククローバー",
        "image": "https://cdn.myanimelist.net/images/anime/2/88336.jpg",
        "synopsis": "Dans un monde où la magie est tout, Asta, né sans pouvoir magique, aspire à devenir le sorcier le plus puissant du royaume. Avec son grimoire unique et sa détermination inébranlable, il poursuit son rêve.",
        "date_debut": "2017-10-03",
        "date_fin": "2021-03-30",
        "episodes": 170,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 7.16,
        "genres": ["Action", "Comédie", "Fantasy", "Magie", "Shonen"],
        "studios": ["Studio Pierrot"],
        "popularite": 36
    },
    {
        "titre": "Neon Genesis Evangelion",
        "titre_japonais": "新世紀エヴァンゲリオン",
        "image": "https://cdn.myanimelist.net/images/anime/1314/108941.jpg",
        "synopsis": "Dans un monde post-apocalyptique, le jeune Shinji Ikari est recruté par son père pour piloter l'EVA-01, un mecha géant, et combattre des entités mystérieuses appelées Anges. Un anime qui mêle action et introspection psychologique.",
        "date_debut": "1995-10-04",
        "date_fin": "1996-03-27",
        "episodes": 26,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.35,
        "genres": ["Action", "Drame", "Mecha", "Psychologique", "Sci-Fi"],
        "studios": ["Gainax"],
        "popularite": 33
    },
    {
        "titre": "Parasyte",
        "titre_japonais": "寄生獣 セイの格率",
        "image": "https://cdn.myanimelist.net/images/anime/3/73178.jpg",
        "synopsis": "Des parasites extraterrestres envahissent la Terre et prennent le contrôle du cerveau humain. Shinichi Izumi est infecté au bras droit, conservant sa conscience. Lui et son parasite, Migi, doivent coexister et lutter contre d'autres parasites.",
        "date_debut": "2014-10-09",
        "date_fin": "2015-03-26",
        "episodes": 24,
        "duree": "22 minutes par épisode",
        "status": "Terminé",
        "score": 8.36,
        "genres": ["Action", "Drame", "Horreur", "Psychologique", "Sci-Fi", "Seinen"],
        "studios": ["Madhouse"],
        "popularite": 37
    },
    {
        "titre": "The Promised Neverland",
        "titre_japonais": "約束のネバーランド",
        "image": "https://cdn.myanimelist.net/images/anime/1125/96929.jpg",
        "synopsis": "Emma, Norman et Ray, orphelins dans une maison idyllique, découvrent l'horrible vérité derrière leur existence : ils sont élevés comme du bétail pour être mangés par des démons. Ils planifient alors leur évasion.",
        "date_debut": "2019-01-10",
        "date_fin": "2019-03-29",
        "episodes": 12,
        "duree": "22 minutes par épisode",
        "status": "Terminé",
        "score": 8.55,
        "genres": ["Horreur", "Mystery", "Psychologique", "Sci-Fi", "Shonen", "Thriller"],
        "studios": ["CloverWorks"],
        "popularite": 39
    },
    {
        "titre": "Food Wars!",
        "titre_japonais": "食戟のソーマ",
        "image": "https://cdn.myanimelist.net/images/anime/3/72943.jpg",
        "synopsis": "Soma Yukihira intègre une prestigieuse école culinaire où seulement 10% des élèves sont diplômés. Avec ses techniques de cuisine innovantes et son audace, il affronte les meilleurs dans des duels culinaires épiques.",
        "date_debut": "2015-04-04",
        "date_fin": "2015-09-26",
        "episodes": 24,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.25,
        "genres": ["Comédie", "Ecchi", "École", "Shonen"],
        "studios": ["J.C.Staff"],
        "popularite": 40
    },
    {
        "titre": "Monster",
        "titre_japonais": "モンスター",
        "image": "https://cdn.myanimelist.net/images/anime/10/18793.jpg",
        "synopsis": "Le Dr Kenzo Tenma, un neurochirurgien brillant, sauve la vie d'un jeune garçon au lieu d'un politicien. Des années plus tard, il découvre que ce garçon est devenu un psychopathe, et part à sa recherche pour réparer son erreur.",
        "date_debut": "2004-04-07",
        "date_fin": "2005-09-28",
        "episodes": 74,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.67,
        "genres": ["Drame", "Horreur", "Mystère", "Psychologique", "Seinen", "Thriller"],
        "studios": ["Madhouse"],
        "popularite": 45
    },
    {
        "titre": "Berserk",
        "titre_japonais": "ベルセルク",
        "image": "https://cdn.myanimelist.net/images/anime/1384/119011.jpg",
        "synopsis": "Guts, un mercenaire solitaire, rejoint la Troupe du Faucon dirigée par le charismatique Griffith. Leur amitié se transforme en une lutte pour la survie lorsque l'ambition de Griffith mène à une trahison indicible.",
        "date_debut": "1997-10-08",
        "date_fin": "1998-04-01",
        "episodes": 25,
        "duree": "25 minutes par épisode",
        "status": "Terminé",
        "score": 8.57,
        "genres": ["Action", "Aventure", "Drame", "Fantasy", "Horreur", "Surnaturel", "Militaire", "Seinen"],
        "studios": ["OLM"],
        "popularite": 41
    },
    {
        "titre": "Psycho-Pass",
        "titre_japonais": "サイコパス",
        "image": "https://cdn.myanimelist.net/images/anime/5/43399.jpg",
        "synopsis": "Dans un futur où un système informatique mesure les tendances criminelles des citoyens, l'inspectrice Akane Tsunemori et l'exécuteur Shinya Kogami traquent un criminel qui échappe au système.",
        "date_debut": "2012-10-12",
        "date_fin": "2013-03-22",
        "episodes": 22,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.34,
        "genres": ["Action", "Policier", "Psychologique", "Sci-Fi", "Thriller"],
        "studios": ["Production I.G"],
        "popularite": 42
    },
    {
        "titre": "Bakemonogatari",
        "titre_japonais": "化物語",
        "image": "https://cdn.myanimelist.net/images/anime/11/75274.jpg",
        "synopsis": "Koyomi Araragi, un lycéen qui a survécu à une attaque de vampire, rencontre plusieurs filles affectées par des \"aberrations\", des anomalies surnaturelles liées à leurs émotions et traumas personnels.",
        "date_debut": "2009-07-03",
        "date_fin": "2010-06-25",
        "episodes": 15,
        "duree": "25 minutes par épisode",
        "status": "Terminé",
        "score": 8.36,
        "genres": ["Comédie", "Drame", "Mystery", "Romance", "Surnaturel", "Vampire"],
        "studios": ["Shaft"],
        "popularite": 43
    },
    {
        "titre": "A Silent Voice",
        "titre_japonais": "聲の形",
        "image": "https://cdn.myanimelist.net/images/anime/1122/96435.jpg",
        "synopsis": "Shoya Ishida, qui a harcelé une camarade malentendante, Shoko Nishimiya, au primaire, cherche à se racheter des années plus tard. Un récit émouvant sur le harcèlement, le pardon et la rédemption.",
        "date_debut": "2016-09-17",
        "date_fin": "2016-09-17",
        "episodes": 1,
        "duree": "130 minutes",
        "status": "Terminé",
        "score": 8.94,
        "genres": ["Drame", "Romance", "École"],
        "studios": ["Kyoto Animation"],
        "popularite": 44
    },
    {
        "titre": "Black Lagoon",
        "titre_japonais": "ブラック・ラグーン",
        "image": "https://cdn.myanimelist.net/images/anime/1906/121592.jpg",
        "synopsis": "Rokuro \"Rock\" Okajima, un homme d'affaires japonais, est kidnappé par des pirates mercenaires dans les eaux de l'Asie du Sud-Est. Finalement accepté dans leur groupe, il découvre un monde de violence et de crime.",
        "date_debut": "2006-04-09",
        "date_fin": "2006-06-25",
        "episodes": 12,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 8.07,
        "genres": ["Action", "Adventure", "Crime", "Drame", "Seinen", "Thriller"],
        "studios": ["Madhouse"],
        "popularite": 48
    },
    {
        "titre": "Bleach",
        "titre_japonais": "ブリーチ",
        "image": "https://cdn.myanimelist.net/images/anime/3/40451.jpg",
        "synopsis": "Ichigo Kurosaki obtient les pouvoirs d'un Shinigami (Dieu de la Mort) et doit protéger les humains contre les esprits maléfiques et guider les âmes vers l'au-delà, tout en découvrant les secrets de son propre passé.",
        "date_debut": "2004-10-05",
        "date_fin": "2012-03-27",
        "episodes": 366,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 7.92,
        "genres": ["Action", "Aventure", "Comédie", "Super Pouvoirs", "Surnaturel", "Shonen"],
        "studios": ["Studio Pierrot"],
        "popularite": 46
    },
    {
        "titre": "Fairy Tail",
        "titre_japonais": "フェアリーテイル",
        "image": "https://cdn.myanimelist.net/images/anime/5/18179.jpg",
        "synopsis": "Lucy Heartfilia, une jeune magicienne, rejoint la guilde Fairy Tail et fait équipe avec Natsu, un chasseur de dragon. Ensemble avec leurs amis, ils accomplissent des missions et affrontent des ennemis redoutables.",
        "date_debut": "2009-10-12",
        "date_fin": "2013-03-30",
        "episodes": 175,
        "duree": "24 minutes par épisode",
        "status": "Terminé",
        "score": 7.61,
        "genres": ["Action", "Aventure", "Comédie", "Fantasy", "Magie", "Shonen"],
        "studios": ["A-1 Pictures", "Satelight"],
        "popularite": 47
    },
    {
        "titre": "Erased",
        "titre_japonais": "僕だけがいない街",
        "image": "https://cdn.myanimelist.net/images/anime/10/77957.jpg",
        "synopsis": "Satoru Fujinuma possède un pouvoir qui le renvoie dans le passé juste avant qu'un accident mortel ne se produise. Après le meurtre de sa mère, il est projeté 18 ans en arrière pour empêcher l'enlèvement de ses camarades de classe.",
        "date_debut": "2016-01-08",
        "date_fin": "2016-03-25",
        "episodes": 12,
        "duree": "23 minutes par épisode",
        "status": "Terminé",
        "score": 8.33,
        "genres": ["Mystery", "Psychologique", "Surnaturel", "Thriller"],
        "studios": ["A-1 Pictures"],
        "popularite": 49
    },
    {
        "titre": "Anohana",
        "titre_japonais": "あの日見た花の名前を僕達はまだ知らない。",
        "image": "https://cdn.myanimelist.net/images/anime/5/79697.jpg",
        "synopsis": "Jinta Yadomi, devenu reclus, est hanté par le fantôme de son amie d'enfance Menma. Pour l'aider à passer dans l'au-delà, il doit réunir leur ancien groupe d'amis et réaliser son souhait.",
        "date_debut": "2011-04-15",
        "date_fin": "2011-06-24",
        "episodes": 11,
        "duree": "22 minutes par épisode",
        "status": "Terminé",
        "score": 8.40,
        "genres": ["Drame", "Slice of Life", "Surnaturel"],
        "studios": ["A-1 Pictures"],
        "popularite": 51
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