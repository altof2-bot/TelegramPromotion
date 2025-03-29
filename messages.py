# Messages du bot
WELCOME_MESSAGE = """
🌟 Bot de Publication d'Animes 📺

🚀 Fonctionnalités :
• Publie automatiquement les animes sur les canaux où il est admin.
• Ajoutez un canal avec la commande : /addchannel @NomDuCanal.

• Si le bot renomme la vidéo, il vous laisse directement.
• après envoi @du canal ici @REQUETE_ANIME_30sbot

💰 Tarifs d'abonnement (paiement en étoiles Telegram) :
• 10 étoiles → 3 jours
• 15 étoiles → 1 semaine
• 25 étoiles → 1 mois
• 50 étoiles → 2 mois

🎟 Pour s'abonner et profiter des publications anime, envoyez vos étoiles via le bot. @altof2
"""

HELP_MESSAGE = """
💫 Aide et Informations 💫

📝 Commandes disponibles :
• /start - Démarrer le bot
• /help - Afficher ce message d'aide
• /addchannel - Ajouter un canal (le bot doit être admin)
• /anime - Rechercher des informations sur un anime
• /stats - Voir les statistiques publiques du bot
• /share - Partager le bot avec vos amis

👨‍💻 Commandes Admin :
• /admin - Accéder au panneau d'administration
• /addanime - Ajouter un nouvel anime à la base de données
• /deleteanime - Supprimer un anime de la base de données
• /listanimes - Afficher la liste des animes disponibles


💰 Tarifs d'abonnement (paiement en étoiles Telegram) :
• 10 étoiles → 3 jours
• 15 étoiles → 1 semaine
• 25 étoiles → 1 mois
• 50 étoiles → 2 mois

🎟 Pour s'abonner et profiter des publications anime, envoyez vos étoiles via le bot. @altof2

❓ Besoin d'aide ? Contactez @altof2
"""

ADMIN_PANEL_MESSAGE = """
🎛 Panneau d'administration

Choisissez une action:
- 📢 Diffuser un message
- ➕ Ajouter un canal
- 📊 Liste des canaux
- ❌ Supprimer un canal
- 👥 Gérer les admins
- 📋 Statistiques
"""

BROADCAST_PROMPT = """
📝 Envoyez le message à diffuser.
Supports: texte, image, vidéo, sticker
"""

ADD_CHANNEL_PROMPT = """
➕ Envoyez l'identifiant du canal à ajouter.
Format: @nom_canal ou -100xxxxxxxxxx
⚠️ Le bot doit être administrateur du canal!
"""

ADD_ADMIN_PROMPT = """
👤 Envoyez l'ID de l'utilisateur à ajouter comme administrateur.
"""

CHANNEL_ADDED = "✅ Canal ajouté avec succès! Le bot pourra désormais y publier des messages."
CHANNEL_REMOVED = "❌ Canal supprimé avec succès! Le bot ne publiera plus dans ce canal."
ADMIN_ADDED = "✅ Administrateur ajouté avec succès! Il peut maintenant accéder au panneau admin."
ADMIN_REMOVED = "❌ Administrateur supprimé avec succès!"
BROADCAST_SUCCESS = "✅ Message diffusé avec succès dans tous les canaux!"
ERROR_MESSAGE = "❌ Une erreur est survenue. Veuillez réessayer."
NOT_ADMIN = "⛔️ Vous n'avez pas les droits d'administration."
BOT_NOT_ADMIN = "⚠️ Le bot n'est pas administrateur de ce canal. Veuillez d'abord l'ajouter comme administrateur avant de l'enregistrer."

# Messages pour les badges et accomplissements
BADGE_EARNED = """
🏆 *Félicitations!* 🏆

Vous avez débloqué un nouveau badge:

{emoji} *{nom}*
└ {description}

Continuez ainsi pour débloquer plus de badges et gagner des points!
"""

LEVEL_UP = """
🎉 *Niveau Supérieur!* 🎉

Félicitations! Vous êtes maintenant au niveau:
{emoji} *{nom}*

Vous avez accumulé {points} points.
"""

NEW_BADGE_NOTIFICATION = """
🔔 *Nouveau Badge Disponible!* 🔔

Continuez à utiliser le bot pour débloquer:
{emoji} *{nom}*
└ {description}
"""

STATS_MESSAGE = """
📊 *Statistiques du Bot* 📊

👥 Utilisateurs: {users_count}
📺 Canaux actifs: {active_channels}
📨 Messages traités: {total_messages}
📢 Diffusions envoyées: {total_broadcasts}

⏱ Dernière mise à jour: {last_update}

🔝 *Utilisateurs de Premier Plan* 🔝
{top_users}

🏅 *Badges Populaires* 🏅
{popular_badges}
"""

SHARE_BOT_MESSAGE = """
🔗 *Partagez le Bot!* 🔗

Aidez à faire grandir notre communauté en partageant ce bot avec vos amis:

`https://t.me/{bot_username}`

Chaque partage vous rapporte des points et vous rapproche du badge Ambassadeur! 📢
"""

ANIME_SEARCH_PROMPT = """
🔍 <b>Recherche d'Anime</b>

Envoyez le nom d'un anime pour obtenir ses informations.
Exemple: Naruto, One Piece, Dragon Ball...
"""

ANIME_NOT_FOUND = """
❌ <b>Aucun anime trouvé</b>

Désolé, nous n'avons pas trouvé d'anime correspondant à votre recherche.
Essayez avec un autre nom ou vérifiez l'orthographe.
"""

ANIME_MULTIPLE_RESULTS = """
🔍 <b>Plusieurs résultats trouvés</b>

Veuillez sélectionner un anime parmi les options suivantes:
"""

# Messages pour la gestion des animes (admin)
ANIME_ADMIN_HELP = """
🎬 <b>Gestion des Animes</b>

Commandes disponibles:
• <code>/addanime</code> - Ajouter un nouvel anime
• <code>/deleteanime</code> - Supprimer un anime
• <code>/listanimes</code> - Voir la liste des animes

Format pour ajouter un anime:
<code>/addanime
Titre: Nom de l'anime
Titre japonais: 日本語タイトル
Image: URL de l'image
Synopsis: Description de l'anime...
Date début: YYYY-MM-DD
Date fin: YYYY-MM-DD (ou vide si en cours)
Épisodes: Nombre d'épisodes
Durée: XX minutes par épisode
Status: Terminé/En cours
Score: X.XX (de 0 à 10)
Genres: Genre1, Genre2, Genre3
Studios: Studio1, Studio2</code>
"""

ANIME_ADD_PROMPT = """
📝 <b>Ajouter un nouvel anime</b>

Veuillez copier et remplir le modèle suivant:

<code>Titre: 
Titre japonais: 
Image: 
Synopsis: 
Date début: 
Date fin: 
Épisodes: 
Durée: 
Status: 
Score: 
Genres: 
Studios: </code>

Exemple:
<code>Titre: My Hero Academia
Titre japonais: 僕のヒーローアカデミア
Image: https://cdn.myanimelist.net/images/anime/10/78745.jpg
Synopsis: Dans un monde où 80% de la population possède des super-pouvoirs...
Date début: 2016-04-03
Date fin: 
Épisodes: 113
Durée: 23 minutes par épisode
Status: En cours
Score: 8.23
Genres: Action, Comédie, Super Pouvoirs, École, Shonen
Studios: Bones</code>
"""

ANIME_DELETE_PROMPT = """
❌ <b>Supprimer un anime</b>

Veuillez sélectionner l'anime à supprimer:
"""

ANIME_LIST_HEADING = """
📋 <b>Liste des Animes</b> (Total: {total})

"""

ANIME_ADDED_SUCCESS = """
✅ <b>Anime ajouté avec succès!</b>

L'anime <b>{titre}</b> a été ajouté à la base de données.
"""

ANIME_ADDED_ERROR = """
❌ <b>Erreur lors de l'ajout de l'anime</b>

{error}

Veuillez vérifier le format et réessayer.
"""

ANIME_DELETED_SUCCESS = """
✅ <b>Anime supprimé avec succès!</b>

L'anime <b>{titre}</b> a été supprimé de la base de données.
"""

ANIME_DELETED_ERROR = """
❌ <b>Erreur lors de la suppression de l'anime</b>

{error}
"""