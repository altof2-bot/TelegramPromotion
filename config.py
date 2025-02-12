import os

# Configuration du bot
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')  # Token sera fourni via les variables d'environnement
ADMIN_ID = 5116530698  # ID de l'administrateur principal

# Messages de log
LOG_START = "Bot démarré"
LOG_ADMIN_ACCESS = "Accès au panneau admin par {}"
LOG_BROADCAST = "Diffusion effectuée par {}"
LOG_CHANNEL_ADD = "Canal ajouté: {}"
LOG_CHANNEL_REMOVE = "Canal supprimé: {}"
LOG_ADMIN_ADD = "Administrateur ajouté: {}"
LOG_ADMIN_REMOVE = "Administrateur supprimé: {}"

# États de conversation
ATTENTE_DIFFUSION = "ATTENTE_DIFFUSION"
ATTENTE_AJOUT_CANAL = "ATTENTE_AJOUT_CANAL"
ATTENTE_AJOUT_ADMIN = "ATTENTE_AJOUT_ADMIN"