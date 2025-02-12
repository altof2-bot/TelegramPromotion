# Messages du bot
WELCOME_MESSAGE = """
🌟 Bot de Publication d'Animes 📺

🚀 Fonctionnalités :
• Publie automatiquement les animes sur les canaux où il est admin.
• Ajoutez un canal avec la commande : /addchannel @NomDuCanal.

• Si le bot renomme la vidéo, il vous laisse directement.
• après envoi @du canal ici @REQUETE_ANIME_30sbot

💰 Tarifs d'abonnement (paiement en étoiles Telegram) :
•10 étoiles → 3 jours
• 15 étoiles → 1 semaine
• 25 étoiles → 1 mois
•50 étoiles → 2 mois

🎟 Pour s'abonner et profiter des publications anime, envoyez vos étoiles via le bot. @altof2
"""

HELP_MESSAGE = """
💫 Aide et Informations 💫

📝 Commandes disponibles :
• /start - Démarrer le bot
• /help - Afficher ce message d'aide
• /addchannel - Ajouter un canal (le bot doit être admin)

💰 Tarifs d'abonnement (paiement en étoiles Telegram) :
•10 étoiles → 3 jours
• 15 étoiles → 1 semaine
• 25 étoiles → 1 mois
•50 étoiles → 2 mois

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