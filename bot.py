from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import ALL, COMMAND
from config import TOKEN
from handlers import start, admin_command, button_callback, handle_message, error_handler, addchannel_command, help_command
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

    # Ajout des handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("addchannel", addchannel_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(ALL & ~COMMAND, handle_message))

    # Handler d'erreur
    application.add_error_handler(error_handler)

    # Démarrage du bot
    logger.info("Bot démarré avec succès. En attente des commandes...")
    print("Bot démarré et prêt à recevoir des commandes...")
    application.run_polling()

if __name__ == '__main__':
    main()