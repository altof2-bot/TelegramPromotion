import json
import os
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.channels = set()
        self.admins = {5116530698}  # ID admin principal
        self.users = {}  # Stockage des données utilisateurs
        self.stats = {
            'total_broadcasts': 0,
            'total_messages': 0,
            'users_count': 0,
            'active_channels': 0,
            'last_update': datetime.now().isoformat()
        }
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists('data.json'):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                    self.channels = set(data.get('channels', []))
                    self.admins = set(data.get('admins', [5116530698]))
                    self.users = data.get('users', {})
                    self.stats = data.get('stats', {
                        'total_broadcasts': 0,
                        'total_messages': 0,
                        'users_count': 0,
                        'active_channels': 0,
                        'last_update': datetime.now().isoformat()
                    })
                    
                    # Conversion des ID en string (car json stocke les clés comme des strings)
                    self.users = {str(user_id): user_data for user_id, user_data in self.users.items()}
                    
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")

    def save_data(self):
        try:
            with open('data.json', 'w') as f:
                # Mise à jour des statistiques
                self.update_stats()
                
                json.dump({
                    'channels': list(self.channels),
                    'admins': list(self.admins),
                    'users': self.users,
                    'stats': self.stats
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des données: {e}")

    def update_stats(self):
        """Met à jour les statistiques globales"""
        self.stats['users_count'] = len(self.users)
        self.stats['active_channels'] = len(self.channels)
        self.stats['last_update'] = datetime.now().isoformat()

    def add_channel(self, channel_id):
        if not channel_id:
            raise ValueError("L'identifiant du canal ne peut pas être vide")
        self.channels.add(channel_id)
        self.save_data()

    def remove_channel(self, channel_id):
        if channel_id in self.channels:
            self.channels.discard(channel_id)
            self.save_data()

    def add_admin(self, admin_id):
        try:
            admin_id = int(admin_id)
            self.admins.add(admin_id)
            self.save_data()
        except ValueError:
            raise ValueError("L'ID de l'administrateur doit être un nombre entier")

    def remove_admin(self, admin_id):
        try:
            admin_id = int(admin_id)
            if admin_id != 5116530698:  # Ne pas supprimer l'admin principal
                self.admins.discard(admin_id)
                self.save_data()
        except ValueError:
            raise ValueError("L'ID de l'administrateur doit être un nombre entier")

    def is_admin(self, user_id):
        try:
            return int(user_id) in self.admins
        except (ValueError, TypeError):
            return False

    def get_channels(self):
        return list(self.channels)

    def get_admins(self):
        return list(self.admins)
        
    # Méthodes de gestion des utilisateurs
    def register_user(self, user_id, user_name=None):
        """Enregistre un nouvel utilisateur ou met à jour ses infos"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            self.users[user_id] = {
                'id': user_id,
                'name': user_name,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'points': 0,
                'badges': [],
                'messages_count': 0,
                'subscribed': False,
                'premium': False,
                'shares': 0
            }
            logger.info(f"Nouvel utilisateur enregistré: {user_id}")
        else:
            # Mise à jour des informations
            self.users[user_id]['last_seen'] = datetime.now().isoformat()
            if user_name:
                self.users[user_id]['name'] = user_name
        
        self.save_data()
        return self.users[user_id]
    
    def update_user_activity(self, user_id, message=False, share=False, subscribe=False, premium=False):
        """Met à jour l'activité d'un utilisateur"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        user['last_seen'] = datetime.now().isoformat()
        
        if message:
            user['messages_count'] = user.get('messages_count', 0) + 1
            self.stats['total_messages'] = self.stats.get('total_messages', 0) + 1
        
        if share:
            user['shares'] = user.get('shares', 0) + 1
        
        if subscribe:
            user['subscribed'] = True
        
        if premium:
            user['premium'] = True
        
        self.save_data()
        return True
    
    def get_user_data(self, user_id):
        """Récupère les données d'un utilisateur"""
        user_id = str(user_id)
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Récupère tous les utilisateurs"""
        return list(self.users.values())
    
    # Méthodes de gestion des badges et points
    def add_user_badge(self, user_id, badge):
        """Ajoute un badge à un utilisateur"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            return False
        
        if 'badges' not in self.users[user_id]:
            self.users[user_id]['badges'] = []
        
        self.users[user_id]['badges'].append(badge)
        self.save_data()
        return True
    
    def get_user_badges(self, user_id):
        """Récupère les badges d'un utilisateur"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            return []
        
        return self.users[user_id].get('badges', [])
    
    def add_user_points(self, user_id, points):
        """Ajoute des points à un utilisateur"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            return False
        
        self.users[user_id]['points'] = self.users[user_id].get('points', 0) + points
        self.save_data()
        return True
    
    def get_user_points(self, user_id):
        """Récupère les points d'un utilisateur"""
        user_id = str(user_id)
        
        if user_id not in self.users:
            return 0
        
        return self.users[user_id].get('points', 0)
    
    # Méthodes de statistiques
    def increment_broadcast_count(self):
        """Incrémente le compteur de diffusions"""
        self.stats['total_broadcasts'] = self.stats.get('total_broadcasts', 0) + 1
        self.save_data()
    
    def get_stats(self):
        """Récupère les statistiques globales"""
        return self.stats