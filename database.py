import json
import os

class Database:
    def __init__(self):
        self.channels = set()
        self.admins = {5116530698}  # ID admin principal
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists('data.json'):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                    self.channels = set(data.get('channels', []))
                    self.admins = set(data.get('admins', [5116530698]))
        except Exception as e:
            print(f"Erreur lors du chargement des données: {e}")

    def save_data(self):
        try:
            with open('data.json', 'w') as f:
                json.dump({
                    'channels': list(self.channels),
                    'admins': list(self.admins)
                }, f)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")

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