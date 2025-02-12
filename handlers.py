from telegram import Update
from telegram.ext import ContextTypes
import logging
from config import *
from keyboards import *
from messages import *
from database import Database

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Instance de la base de données
db = Database()

async def addchannel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /addchannel"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans addchannel_command")
        return

    # Extraire l'identifiant du canal de la commande
    args = context.args
    if not args:
        logger.info("Commande /addchannel reçue sans arguments")
        await update.message.reply_text(
            f"{ADD_CHANNEL_PROMPT}\n\nExemple: /addchannel @nom_canal"
        )
        return

    channel_id = args[0]
    try:
        # Log de la tentative d'ajout
        logger.info(f"Tentative d'ajout du canal via /addchannel: {channel_id}")

        if not channel_id.startswith('@') and not channel_id.startswith('-100'):
            logger.warning(f"Format de canal invalide reçu: {channel_id}")
            raise ValueError("Format de canal invalide")

        # Vérifier que le bot est admin du canal
        chat_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=context.bot.id)
        logger.info(f"Statut du bot dans le canal {channel_id}: {chat_member.status}")

        if chat_member.status not in ['administrator', 'creator']:
            logger.warning(f"Le bot n'est pas admin dans le canal {channel_id}")
            await update.message.reply_text(
                f"{BOT_NOT_ADMIN}\n\nStatut actuel : {chat_member.status}"
            )
            return

        # Vérifier si le canal existe déjà
        if channel_id in db.get_channels():
            logger.info(f"Le canal {channel_id} est déjà enregistré")
            await update.message.reply_text("Ce canal est déjà enregistré dans la base de données.")
            return

        # Si le bot est admin et le canal n'existe pas, on l'ajoute
        db.add_channel(channel_id)
        logger.info(LOG_CHANNEL_ADD.format(channel_id))
        await update.message.reply_text(CHANNEL_ADDED)

    except ValueError as ve:
        logger.error(f"Erreur de format pour le canal {channel_id}: {str(ve)}")
        await update.message.reply_text(
            "❌ Format incorrect. Le canal doit commencer par @ ou -100\n\n"
            "Exemple: /addchannel @nom_canal"
        )
    except Exception as e:
        logger.error(f"Erreur lors de l'ajout du canal {channel_id}: {str(e)}")
        error_message = f"{ERROR_MESSAGE}\nErreur: Le canal n'existe pas ou le bot n'y a pas accès."
        await update.message.reply_text(error_message)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start"""
    await update.message.reply_text(WELCOME_MESSAGE)

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /admin"""
    if not update or not update.effective_user:
        logger.error("Utilisateur non trouvé dans la commande admin")
        return

    user_id = update.effective_user.id
    if db.is_admin(user_id):
        logger.info(LOG_ADMIN_ACCESS.format(user_id))
        await update.message.reply_text(
            ADMIN_PANEL_MESSAGE,
            reply_markup=get_admin_keyboard()
        )
    else:
        await update.message.reply_text(NOT_ADMIN)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les callbacks des boutons inline"""
    query = update.callback_query
    if not update.effective_user:
        logger.error("Utilisateur non trouvé dans le callback")
        await query.answer("Erreur: utilisateur non trouvé")
        return

    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await query.answer(NOT_ADMIN)
        return

    await query.answer()

    if query.data == 'diffuser':
        context.user_data['state'] = ATTENTE_DIFFUSION
        await query.message.edit_text(BROADCAST_PROMPT)

    elif query.data == 'ajouter_canal':
        context.user_data['state'] = ATTENTE_AJOUT_CANAL
        await query.message.edit_text(ADD_CHANNEL_PROMPT)

    elif query.data == 'liste_canaux':
        channels = db.get_channels()
        message = "📊 Liste des canaux:\n\n"
        for channel in channels:
            message += f"- {channel}\n"
        if not channels:
            message += "Aucun canal n'est enregistré."
        await query.message.edit_text(
            message,
            reply_markup=get_admin_keyboard()
        )

    elif query.data == 'supprimer_canal':
        channels = db.get_channels()
        if not channels:
            await query.message.edit_text(
                "Aucun canal n'est enregistré.",
                reply_markup=get_admin_keyboard()
            )
            return
        await query.message.edit_text(
            "Sélectionnez le canal à supprimer:",
            reply_markup=get_channel_list_keyboard(channels)
        )

    elif query.data.startswith('select_channel:'):
        channel = query.data.replace('select_channel:', '')
        context.user_data['selected_channel'] = channel
        await query.message.edit_text(
            f"Voulez-vous vraiment supprimer le canal {channel} ?",
            reply_markup=get_confirm_keyboard('delete_channel')
        )

    elif query.data == 'confirm_delete_channel':
        channel = context.user_data.get('selected_channel')
        if channel:
            db.remove_channel(channel)
            logger.info(LOG_CHANNEL_REMOVE.format(channel))
            await query.message.edit_text(
                CHANNEL_REMOVED,
                reply_markup=get_admin_keyboard()
            )
            context.user_data.pop('selected_channel', None)

    elif query.data == 'gerer_admins':
        await query.message.edit_text(
            "Gestion des administrateurs:",
            reply_markup=get_admin_management_keyboard()
        )

    elif query.data == 'liste_admins':
        admins = db.get_admins()
        message = "👥 Liste des administrateurs:\n\n"
        for admin_id in admins:
            message += f"- ID: {admin_id}\n"
        await query.message.edit_text(
            message,
            reply_markup=get_admin_management_keyboard()
        )

    elif query.data == 'ajouter_admin':
        context.user_data['state'] = ATTENTE_AJOUT_ADMIN
        await query.message.edit_text(ADD_ADMIN_PROMPT)

    elif query.data == 'retour_admin':
        await query.message.edit_text(
            ADMIN_PANEL_MESSAGE,
            reply_markup=get_admin_keyboard()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages reçus"""
    if not update or not update.effective_user:
        logger.error("Utilisateur non trouvé dans le message")
        return

    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        return

    state = context.user_data.get('state')

    if state == ATTENTE_DIFFUSION:
        channels = db.get_channels()
        for channel in channels:
            try:
                # Vérifier que le bot est admin du canal
                chat_member = await context.bot.get_chat_member(chat_id=channel, user_id=context.bot.id)
                if chat_member.status not in ['administrator', 'creator']:
                    logger.warning(f"Le bot n'est pas admin dans le canal {channel}")
                    continue

                if update.message.text:
                    await context.bot.send_message(channel, update.message.text)
                elif update.message.photo:
                    await context.bot.send_photo(
                        channel,
                        update.message.photo[-1].file_id,
                        caption=update.message.caption
                    )
                elif update.message.video:
                    await context.bot.send_video(
                        channel,
                        update.message.video.file_id,
                        caption=update.message.caption
                    )
                elif update.message.sticker:
                    await context.bot.send_sticker(
                        channel,
                        update.message.sticker.file_id
                    )
            except Exception as e:
                logger.error(f"Erreur lors de la diffusion vers {channel}: {e}")

        await update.message.reply_text(
            BROADCAST_SUCCESS,
            reply_markup=get_admin_keyboard()
        )
        context.user_data.pop('state', None)

    elif state == ATTENTE_AJOUT_CANAL:
        channel_id = update.message.text
        try:
            # Log de la tentative d'ajout
            logger.info(f"Tentative d'ajout du canal: {channel_id}")

            if not channel_id.startswith('@') and not channel_id.startswith('-100'):
                raise ValueError("Format de canal invalide")

            # Vérifier que le bot est admin du canal
            chat_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=context.bot.id)
            logger.info(f"Statut du bot dans le canal {channel_id}: {chat_member.status}")

            if chat_member.status not in ['administrator', 'creator']:
                logger.warning(f"Le bot n'est pas admin dans le canal {channel_id}")
                await update.message.reply_text(
                    BOT_NOT_ADMIN,
                    reply_markup=get_admin_keyboard()
                )
                context.user_data.pop('state', None)
                return

            # Si le bot est admin, on ajoute le canal
            db.add_channel(channel_id)
            logger.info(LOG_CHANNEL_ADD.format(channel_id))
            await update.message.reply_text(
                CHANNEL_ADDED,
                reply_markup=get_admin_keyboard()
            )
        except ValueError as ve:
            logger.error(f"Erreur de format pour le canal {channel_id}: {str(ve)}")
            await update.message.reply_text(
                f"❌ Format incorrect. Le canal doit commencer par @ ou -100",
                reply_markup=get_admin_keyboard()
            )
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout du canal {channel_id}: {str(e)}")
            error_message = f"{ERROR_MESSAGE}\nErreur: Le canal n'existe pas ou le bot n'y a pas accès."
            await update.message.reply_text(
                error_message,
                reply_markup=get_admin_keyboard()
            )
        context.user_data.pop('state', None)

    elif state == ATTENTE_AJOUT_ADMIN:
        try:
            admin_id = int(update.message.text)
            db.add_admin(admin_id)
            logger.info(LOG_ADMIN_ADD.format(admin_id))
            await update.message.reply_text(
                ADMIN_ADDED,
                reply_markup=get_admin_keyboard()
            )
        except ValueError:
            await update.message.reply_text(
                "❌ L'ID doit être un nombre entier. Veuillez réessayer.",
                reply_markup=get_admin_keyboard()
            )
        context.user_data.pop('state', None)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les erreurs du bot"""
    logger.error(f"Erreur: {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logger.error(f"Erreur dans le gestionnaire d'erreurs: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /help"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans help_command")
        return

    await update.message.reply_text(HELP_MESSAGE)