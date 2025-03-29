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
            InlineKeyboardButton("📈 Statistiques", callback_data='stats')
        ],
        [
            InlineKeyboardButton("🏆 Badges & Niveaux", callback_data='badges_settings'),
            InlineKeyboardButton("🎬 Gérer les animes", callback_data='gerer_animes')
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

def get_badges_management_keyboard():
    """Clavier pour la gestion des badges et accomplissements"""
    keyboard = [
        [
            InlineKeyboardButton("👤 Attribuer un badge", callback_data='attribuer_badge'),
            InlineKeyboardButton("🏅 Créer un badge spécial", callback_data='creer_badge')
        ],
        [
            InlineKeyboardButton("📊 Statistiques badges", callback_data='stats_badges'),
            InlineKeyboardButton("🔙 Retour", callback_data='retour_admin')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_user_profile_keyboard():
    """Clavier pour le profil utilisateur"""
    keyboard = [
        [
            InlineKeyboardButton("🏆 Mes badges", callback_data='view_badges'),
            InlineKeyboardButton("📊 Mon niveau", callback_data='view_level')
        ],
        [
            InlineKeyboardButton("🌟 Classement", callback_data='view_leaderboard'),
            InlineKeyboardButton("📢 Partager le bot", callback_data='share_bot')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_award_badge_keyboard(badges):
    """Clavier pour attribuer un badge à un utilisateur"""
    keyboard = []
    for badge_id, badge in badges.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{badge['emoji']} {badge['nom']}",
                callback_data=f'award_badge:{badge_id}'
            )
        ])
    keyboard.append([InlineKeyboardButton("🔙 Retour", callback_data='badges_settings')])
    return InlineKeyboardMarkup(keyboard)

def get_user_selection_keyboard(users, callback_prefix, page=0, per_page=5):
    """Clavier paginé pour sélectionner un utilisateur"""
    keyboard = []
    
    # Calculer les indices de début et de fin pour la pagination
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, len(users))
    
    # Ajouter les boutons pour les utilisateurs de la page actuelle
    for i in range(start_idx, end_idx):
        user = users[i]
        user_name = user.get('name', f"Utilisateur {user['id']}")
        keyboard.append([
            InlineKeyboardButton(
                f"{user_name} (ID: {user['id']})",
                callback_data=f'{callback_prefix}:{user["id"]}'
            )
        ])
    
    # Ajouter les boutons de navigation de pagination si nécessaire
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("⬅️ Précédent", callback_data=f'page:{callback_prefix}:{page-1}')
        )
    
    if end_idx < len(users):
        nav_buttons.append(
            InlineKeyboardButton("➡️ Suivant", callback_data=f'page:{callback_prefix}:{page+1}')
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Bouton de retour
    keyboard.append([InlineKeyboardButton("🔙 Retour", callback_data='badges_settings')])
    
    return InlineKeyboardMarkup(keyboard)

def get_stats_keyboard():
    """Clavier pour la page de statistiques"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Statistiques générales", callback_data='stats_general'),
            InlineKeyboardButton("👥 Utilisateurs", callback_data='stats_users')
        ],
        [
            InlineKeyboardButton("🏆 Badges", callback_data='stats_badges'),
            InlineKeyboardButton("📈 Activité", callback_data='stats_activity')
        ],
        [
            InlineKeyboardButton("🔙 Retour", callback_data='retour_admin')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def get_anime_selection_keyboard(animes, online_search=False):
    """Clavier pour sélectionner un anime parmi plusieurs résultats"""
    keyboard = []
    
    for i, anime in enumerate(animes):
        keyboard.append([
            InlineKeyboardButton(
                f"{anime['titre']}{' 🌐' if anime.get('source') == 'api' else ''}",
                callback_data=f"anime:{anime['id']}"
            )
        ])
    
    # Si une recherche en ligne supplémentaire est possible, ajouter un bouton
    if online_search:
        keyboard.append([
            InlineKeyboardButton(
                "🔍 Rechercher en ligne", 
                callback_data="search_online"
            )
        ])
    
    # Bouton d'annulation
    keyboard.append([InlineKeyboardButton("❌ Annuler", callback_data='annuler_recherche')])
    
    return InlineKeyboardMarkup(keyboard)

def get_anime_management_keyboard():
    """Clavier pour la gestion des animes (admin)"""
    keyboard = [
        [
            InlineKeyboardButton("➕ Ajouter un anime", callback_data='ajouter_anime'),
            InlineKeyboardButton("❌ Supprimer un anime", callback_data='supprimer_anime')
        ],
        [
            InlineKeyboardButton("📋 Liste des animes", callback_data='liste_animes'),
            InlineKeyboardButton("🔍 Rechercher", callback_data='rechercher_anime_admin')
        ],
        [
            InlineKeyboardButton("🔙 Retour", callback_data='retour_admin')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_anime_list_keyboard(animes, page=0, per_page=5, for_deletion=False):
    """Clavier paginé pour afficher une liste d'animes"""
    keyboard = []
    
    # Calculer les indices de début et de fin pour la pagination
    start_idx = page * per_page
    end_idx = min(start_idx + per_page, len(animes))
    
    # Callback prefix en fonction de l'utilisation (suppression ou vue détaillée)
    callback_prefix = 'delete_anime' if for_deletion else 'view_anime'
    
    # Ajouter les boutons pour les animes de la page actuelle
    for i in range(start_idx, end_idx):
        anime = animes[i]
        keyboard.append([
            InlineKeyboardButton(
                f"{anime['titre']} (ID: {anime['id']})",
                callback_data=f'{callback_prefix}:{anime["id"]}'
            )
        ])
    
    # Ajouter les boutons de navigation de pagination si nécessaire
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton("⬅️ Précédent", callback_data=f'animes_page:{callback_prefix}:{page-1}')
        )
    
    if end_idx < len(animes):
        nav_buttons.append(
            InlineKeyboardButton("➡️ Suivant", callback_data=f'animes_page:{callback_prefix}:{page+1}')
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Bouton de retour
    keyboard.append([InlineKeyboardButton("🔙 Retour", callback_data='gerer_animes')])
    
    return InlineKeyboardMarkup(keyboard)