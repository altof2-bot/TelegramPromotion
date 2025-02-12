# Messages du bot
WELCOME_MESSAGE = """
👋 Bienvenue sur le bot de gestion des canaux!
Pour accéder au panneau d'administration, utilisez /admin
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
Supports: texte, image, vidéo
"""

ADD_CHANNEL_PROMPT = """
➕ Envoyez l'identifiant du canal à ajouter.
Format: @nom_canal ou -100xxxxxxxxxx
"""

ADD_ADMIN_PROMPT = """
👤 Envoyez l'ID de l'utilisateur à ajouter comme administrateur.
"""

CHANNEL_ADDED = "✅ Canal ajouté avec succès!"
CHANNEL_REMOVED = "❌ Canal supprimé avec succès!"
ADMIN_ADDED = "✅ Administrateur ajouté avec succès!"
ADMIN_REMOVED = "❌ Administrateur supprimé avec succès!"
BROADCAST_SUCCESS = "✅ Message diffusé avec succès!"
ERROR_MESSAGE = "❌ Une erreur est survenue. Veuillez réessayer."
NOT_ADMIN = "⛔️ Vous n'avez pas les droits d'administration."
