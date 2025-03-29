from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import ALL, COMMAND
from config import TOKEN
from handlers import (
    start, admin_command, button_callback, handle_message, error_handler, 
    addchannel_command, help_command, stats_command, share_command, anime_command,
    addanime_command, deleteanime_command, listanimes_command
)
import logging

def main():
    # Configuration du logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # Création de l'application
    application = ApplicationBuilder().token(TOKEN).build()

    # Ajout des handlers pour les commandes de base
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("addchannel", addchannel_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Ajout des handlers pour les fonctionnalités supplémentaires
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("share", share_command))
    application.add_handler(CommandHandler("anime", anime_command))
    
    # Ajout des handlers pour la gestion des animes (admin)
    application.add_handler(CommandHandler("addanime", addanime_command))
    application.add_handler(CommandHandler("deleteanime", deleteanime_command))
    application.add_handler(CommandHandler("listanimes", listanimes_command))
    
    # Ajout du handler pour les callbacks de boutons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Handler pour les messages qui ne sont pas des commandes
    application.add_handler(MessageHandler(ALL & ~COMMAND, handle_message))

    # Handler d'erreur
    application.add_error_handler(error_handler)

    # Démarrage du bot
    logger.info("Bot démarré avec succès. En attente des commandes...")
    print("Bot démarré et prêt à recevoir des commandes...")
    application.run_polling()

if __name__ == '__main__':
    main()