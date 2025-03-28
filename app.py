from flask import Flask
from threading import Thread
from bot import main as bot_main
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot Telegram actif!'

@app.route('/ping')
def ping():
    return 'pong'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

def keep_alive():
    server = Thread(target=run)
    server.start()

if __name__ == "__main__":
    # Démarrer le serveur Flask dans un thread séparé
    keep_alive()
    # Démarrer le bot Telegram dans le thread principal
    bot_main()
