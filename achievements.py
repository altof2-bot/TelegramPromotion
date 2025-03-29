"""
Module de gestion des badges et accomplissements pour la gamification
"""
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Définition des badges disponibles
BADGES = {
    'nouveau_membre': {
        'id': 'nouveau_membre',
        'nom': 'Nouveau Membre',
        'emoji': '🔰',
        'description': 'A rejoint le bot de publication anime',
        'points': 5
    },
    'abonne': {
        'id': 'abonne',
        'nom': 'Abonné',
        'emoji': '🌟',
        'description': 'S\'est abonné à un canal anime',
        'points': 10
    },
    'partage': {
        'id': 'partage',
        'nom': 'Ambassadeur',
        'emoji': '📢',
        'description': 'A partagé le bot avec d\'autres utilisateurs',
        'points': 15
    },
    'fidele': {
        'id': 'fidele',
        'nom': 'Utilisateur Fidèle',
        'emoji': '🏆',
        'description': 'Utilise le bot depuis plus d\'une semaine',
        'points': 20
    },
    'premium': {
        'id': 'premium',
        'nom': 'Membre Premium',
        'emoji': '💎',
        'description': 'A souscrit à un abonnement premium',
        'points': 30
    }
}

# Niveaux utilisateur basés sur les points
NIVEAUX = {
    0: {'nom': 'Débutant', 'emoji': '🥉', 'points_requis': 0},
    1: {'nom': 'Régulier', 'emoji': '🥈', 'points_requis': 20},
    2: {'nom': 'Passionné', 'emoji': '🥇', 'points_requis': 50},
    3: {'nom': 'Expert', 'emoji': '🏅', 'points_requis': 100},
    4: {'nom': 'Légende', 'emoji': '👑', 'points_requis': 200}
}

class AchievementManager:
    """Gestionnaire des badges et accomplissements"""
    
    def __init__(self, db):
        """Initialise le gestionnaire avec une référence à la base de données"""
        self.db = db
    
    def award_badge(self, user_id, badge_id):
        """Attribue un badge à un utilisateur"""
        if badge_id not in BADGES:
            logger.error(f"Badge inconnu: {badge_id}")
            return False
        
        # Vérifier si l'utilisateur a déjà ce badge
        user_badges = self.db.get_user_badges(user_id)
        if badge_id in [b['id'] for b in user_badges]:
            logger.info(f"L'utilisateur {user_id} possède déjà le badge {badge_id}")
            return False
        
        # Ajouter le badge à l'utilisateur
        badge = BADGES[badge_id].copy()
        badge['date_obtention'] = datetime.now().isoformat()
        
        # Ajouter le badge et les points associés
        self.db.add_user_badge(user_id, badge)
        self.db.add_user_points(user_id, badge['points'])
        
        logger.info(f"Badge {badge_id} attribué à l'utilisateur {user_id}")
        return True
    
    def check_badge_eligibility(self, user_id):
        """Vérifie si l'utilisateur est éligible à de nouveaux badges"""
        awarded_badges = []
        
        # Vérifier chaque règle de badge
        user_data = self.db.get_user_data(user_id)
        
        # Badge nouveau membre (si première interaction)
        if not user_data or not user_data.get('badges'):
            if self.award_badge(user_id, 'nouveau_membre'):
                awarded_badges.append(BADGES['nouveau_membre'])
        
        # Badge utilisateur fidèle (si inscription il y a plus d'une semaine)
        if user_data and user_data.get('first_seen'):
            first_seen = datetime.fromisoformat(user_data['first_seen'])
            now = datetime.now()
            days_difference = (now - first_seen).days
            
            if days_difference >= 7 and self.award_badge(user_id, 'fidele'):
                awarded_badges.append(BADGES['fidele'])
        
        # Si l'utilisateur a effectué un abonnement
        if user_data and user_data.get('subscribed'):
            if self.award_badge(user_id, 'abonne'):
                awarded_badges.append(BADGES['abonne'])
        
        # Si l'utilisateur a partagé le bot
        if user_data and user_data.get('shares', 0) > 0:
            if self.award_badge(user_id, 'partage'):
                awarded_badges.append(BADGES['partage'])
        
        # Si l'utilisateur a un abonnement premium
        if user_data and user_data.get('premium'):
            if self.award_badge(user_id, 'premium'):
                awarded_badges.append(BADGES['premium'])
        
        return awarded_badges
    
    def get_user_level(self, user_id):
        """Obtient le niveau actuel de l'utilisateur basé sur ses points"""
        points = self.db.get_user_points(user_id)
        
        user_level = 0
        for level, data in sorted(NIVEAUX.items(), reverse=True):
            if points >= data['points_requis']:
                user_level = level
                break
        
        return {
            'niveau': user_level,
            'nom': NIVEAUX[user_level]['nom'],
            'emoji': NIVEAUX[user_level]['emoji'],
            'points': points,
            'prochain_niveau': min(user_level + 1, max(NIVEAUX.keys())),
            'points_prochain': NIVEAUX[min(user_level + 1, max(NIVEAUX.keys()))]['points_requis'] if user_level < max(NIVEAUX.keys()) else None
        }
    
    def format_user_progress(self, user_id):
        """Formate un message affichant la progression de l'utilisateur"""
        user_badges = self.db.get_user_badges(user_id)
        level_info = self.get_user_level(user_id)
        
        # Construire le message
        message = f"📊 *Votre Progression* 📊\n\n"
        message += f"{level_info['emoji']} Niveau: *{level_info['nom']}*\n"
        message += f"🔄 Points: *{level_info['points']}*"
        
        if level_info['prochain_niveau'] > level_info['niveau']:
            points_needed = level_info['points_prochain'] - level_info['points']
            message += f" ({points_needed} points pour le niveau suivant)\n"
        else:
            message += " (Niveau maximum atteint!)\n"
        
        # Ajouter les badges
        message += "\n🏅 *Vos Badges* 🏅\n"
        if user_badges:
            for badge in user_badges:
                date_str = datetime.fromisoformat(badge['date_obtention']).strftime('%d/%m/%Y')
                message += f"\n{badge['emoji']} *{badge['nom']}*"
                message += f"\n└ {badge['description']}"
                message += f"\n└ Obtenu le: {date_str}"
        else:
            message += "\nVous n'avez pas encore de badges. Continuez à utiliser le bot pour en obtenir!"
        
        # Ajouter des badges à débloquer
        all_badge_ids = set(BADGES.keys())
        user_badge_ids = set(badge['id'] for badge in user_badges)
        locked_badge_ids = all_badge_ids - user_badge_ids
        
        if locked_badge_ids:
            message += "\n\n🔒 *Badges à Débloquer* 🔒\n"
            for badge_id in locked_badge_ids:
                badge = BADGES[badge_id]
                message += f"\n{badge['emoji']} *{badge['nom']}*"
                message += f"\n└ {badge['description']}"
        
        return message
    
    def get_leaderboard(self, limit=10):
        """Récupère le classement des utilisateurs par points"""
        users = self.db.get_all_users()
        
        # Trier les utilisateurs par points
        sorted_users = sorted(users, key=lambda u: u.get('points', 0), reverse=True)
        
        # Limiter le nombre d'utilisateurs
        leaderboard = sorted_users[:limit]
        
        # Formatter le classement
        message = "🏆 *Classement des Utilisateurs* 🏆\n\n"
        
        for i, user in enumerate(leaderboard, 1):
            level_info = self.get_user_level(user['id'])
            badges_count = len(user.get('badges', []))
            
            user_name = user.get('name', f"Utilisateur {user['id']}")
            message += f"{i}. {level_info['emoji']} *{user_name}*\n"
            message += f"   └ Niveau: {level_info['nom']} | Points: {user.get('points', 0)} | Badges: {badges_count}\n"
        
        if not leaderboard:
            message += "Aucun utilisateur classé pour le moment."
        
        # Statistiques globales
        total_users = len(users)
        total_badges = sum(len(user.get('badges', [])) for user in users)
        
        message += f"\n📈 *Statistiques Globales* 📈\n"
        message += f"👥 Utilisateurs: {total_users}\n"
        message += f"🏅 Badges distribués: {total_badges}"
        
        return message