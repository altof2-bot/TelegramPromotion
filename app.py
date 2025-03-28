from flask import Flask
from threading import Thread
import os
import sys
import logging

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot Telegram actif!'

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/health')
def health():
    return 'ok', 200

# Cette fonction démarrera le bot séparément pour Koyeb
def start_bot():
    try:
        from bot import main as bot_main
        logger.info("Démarrage du bot Telegram...")
        bot_main()
    except Exception as e:
        logger.error(f"Erreur lors du démarrage du bot: {e}")
        sys.exit(1)

# Exécuter Flask directement avec Gunicorn sur Koyeb
if __name__ == "__main__":
    # Vérifier si nous devons démarrer le bot ou le serveur web
    if len(sys.argv) > 1 and sys.argv[1] == "bot":
        # Mode bot pour le worker
        start_bot()
    else:
        # Mode serveur web pour le web service
        port = int(os.environ.get('PORT', 3000))
        app.run(host='0.0.0.0', port=port)
