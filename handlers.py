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
            except Exception as e:
                logger.error(f"Erreur lors de la diffusion vers {channel}: {e}")

        await update.message.reply_text(
            BROADCAST_SUCCESS,
            reply_markup=get_admin_keyboard()
        )
        context.user_data.pop('state', None)

    elif state == ATTENTE_AJOUT_CANAL:
        channel_id = update.message.text
        db.add_channel(channel_id)
        logger.info(LOG_CHANNEL_ADD.format(channel_id))
        await update.message.reply_text(
            CHANNEL_ADDED,
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