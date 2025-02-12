from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_keyboard():
    """Clavier principal du panneau admin avec toutes les fonctionnalités"""
    keyboard = [
        [
            InlineKeyboardButton("📢 Diffuser un message", callback_data='diffuser'),
            InlineKeyboardButton("➕ Ajouter un canal", callback_data='ajouter_canal')
        ],
        [
            InlineKeyboardButton("📊 Liste des canaux", callback_data='liste_canaux'),
            InlineKeyboardButton("❌ Supprimer un canal", callback_data='supprimer_canal')
        ],
        [
            InlineKeyboardButton("👥 Gérer les admins", callback_data='gerer_admins'),
            InlineKeyboardButton("📋 Statistiques", callback_data='stats')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_channel_list_keyboard(channels):
    """Clavier pour afficher la liste des canaux avec option de sélection"""
    keyboard = []
    for channel in channels:
        keyboard.append([InlineKeyboardButton(channel, callback_data=f'select_channel:{channel}')])
    keyboard.append([InlineKeyboardButton("🔙 Retour", callback_data='retour_admin')])
    return InlineKeyboardMarkup(keyboard)

def get_admin_management_keyboard():
    """Clavier pour la gestion des administrateurs"""
    keyboard = [
        [
            InlineKeyboardButton("➕ Ajouter un admin", callback_data='ajouter_admin'),
            InlineKeyboardButton("❌ Supprimer un admin", callback_data='supprimer_admin')
        ],
        [
            InlineKeyboardButton("📊 Liste des admins", callback_data='liste_admins'),
            InlineKeyboardButton("🔙 Retour", callback_data='retour_admin')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirm_keyboard(action_id):
    """Clavier de confirmation pour les actions importantes"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirmer", callback_data=f'confirm_{action_id}'),
            InlineKeyboardButton("❌ Annuler", callback_data='retour_admin')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)