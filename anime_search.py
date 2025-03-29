"""
Module pour rechercher des informations sur les animes.
Utilise l'API Jikan (MyAnimeList) pour obtenir les données depuis internet.
"""

import requests
import logging
from datetime import datetime
import html
import time

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

JIKAN_API_URL = "https://api.jikan.moe/v4"

def search_anime_online(query, limit=5):
    """
    Recherche un anime par nom via l'API Jikan (MyAnimeList)
    
    Args:
        query (str): Le nom de l'anime à rechercher
        limit (int): Nombre maximum de résultats (défaut: 5)
        
    Returns:
        list: Liste des animes correspondants à la recherche
    """
    try:
        url = f"{JIKAN_API_URL}/anime"
        params = {
            "q": query,
            "limit": limit,
            "sfw": True  # Contenu sûr pour le travail
        }
        
        # L'API Jikan limite le nombre de requêtes par seconde
        time.sleep(0.5)  
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        
        data = response.json()
        
        # Transformer les données de l'API au format compatible avec notre application
        results = []
        for anime in data.get('data', []):
            formatted_anime = {
                'id': anime.get('mal_id'),
                'titre': anime.get('title', 'Inconnu'),
                'titre_japonais': anime.get('title_japanese', 'Inconnu'),
                'image': anime.get('images', {}).get('jpg', {}).get('image_url', ''),
                'synopsis': anime.get('synopsis', 'Aucune description disponible.'),
                'date_debut': anime.get('aired', {}).get('from', ''),
                'date_fin': anime.get('aired', {}).get('to', ''),
                'episodes': anime.get('episodes', 'Inconnu'),
                'duree': anime.get('duration', 'Inconnu'),
                'status': anime.get('status', 'Inconnu'),
                'score': anime.get('score', 0),
                'popularite': anime.get('popularity', 0),
                'genres': [g.get('name', '') for g in anime.get('genres', [])],
                'studios': [s.get('name', '') for s in anime.get('studios', [])],
                'source': 'api',  # Indique que c'est une source en ligne
                'url': anime.get('url', '')  # Lien vers MyAnimeList
            }
            results.append(formatted_anime)
            
        return results
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la recherche d'anime en ligne: {e}")
        return []
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la recherche d'anime en ligne: {e}")
        return []

def get_anime_details(anime_id):
    """
    Obtient les détails complets d'un anime par son ID
    
    Args:
        anime_id (int): L'ID de l'anime
        
    Returns:
        dict: Les détails de l'anime ou None en cas d'erreur
    """
    try:
        url = f"{JIKAN_API_URL}/anime/{anime_id}/full"
        
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data')
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la récupération des détails de l'anime: {e}")
        return None

def format_anime_message(anime):
    """
    Formate les informations d'un anime pour l'affichage dans Telegram
    
    Args:
        anime (dict): Les données de l'anime
        
    Returns:
        str: Message formaté pour Telegram
    """
    try:
        # Échappement des caractères spéciaux pour Markdown
        title = html.escape(anime.get('title', 'Inconnu'))
        title_japanese = html.escape(anime.get('title_japanese', 'Inconnu'))
        synopsis = html.escape(anime.get('synopsis', 'Aucune description disponible.'))
        if len(synopsis) > 300:
            synopsis = synopsis[:297] + "..."
            
        # Informations de base
        message = f"<b>📺 {title}</b>\n"
        message += f"<b>🇯🇵 Titre japonais:</b> {title_japanese}\n\n"
        
        # Score et popularité
        score = anime.get('score', 'N/A')
        popularity = anime.get('popularity', 'N/A')
        message += f"<b>⭐ Score:</b> {score} | <b>👥 Popularité:</b> #{popularity}\n"
        
        # Statut et dates
        status = anime.get('status', 'Inconnu')
        
        # Formatage des dates
        aired = anime.get('aired', {})
        from_date = aired.get('from', '')
        to_date = aired.get('to', '')
        
        # Convertir les dates en format lisible
        date_format = ""
        if from_date:
            try:
                from_date = datetime.fromisoformat(from_date.replace('Z', '+00:00'))
                date_format = from_date.strftime("%d/%m/%Y")
            except (ValueError, TypeError):
                date_format = "?"
                
        if to_date:
            try:
                to_date = datetime.fromisoformat(to_date.replace('Z', '+00:00'))
                date_format += f" → {to_date.strftime('%d/%m/%Y')}"
            except (ValueError, TypeError):
                date_format += " → ?"
        elif status == "Currently Airing":
            date_format += " → En cours"
            
        message += f"<b>📆 Diffusion:</b> {date_format}\n"
        
        # Épisodes et durée
        episodes = anime.get('episodes', 'Inconnu')
        duration = anime.get('duration', 'Inconnu')
        message += f"<b>🎬 Épisodes:</b> {episodes} | <b>⏱ Durée:</b> {duration}\n"
        
        # Genres
        genres = anime.get('genres', [])
        if genres:
            genre_names = [g.get('name', '') for g in genres]
            message += f"<b>🏷️ Genres:</b> {', '.join(genre_names)}\n"
            
        # Studios
        studios = anime.get('studios', [])
        if studios:
            studio_names = [s.get('name', '') for s in studios]
            message += f"<b>🎨 Studios:</b> {', '.join(studio_names)}\n"
            
        # Synopsis
        message += f"\n<b>📝 Synopsis:</b>\n{synopsis}\n"
        
        # URL vers la page MyAnimeList
        url = anime.get('url', '')
        if url:
            message += f"\n<a href='{url}'>Plus d'informations sur MyAnimeList</a>"
            
        return message
    except Exception as e:
        logger.error(f"Erreur lors du formatage du message: {e}")
        return "Erreur lors du formatage des informations de l'anime."