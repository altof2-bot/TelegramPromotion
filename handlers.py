from telegram import Update
from telegram.ext import ContextTypes
import logging
from datetime import datetime
import re
from config import *
from keyboards import *
from messages import *
from database import Database
import achievements
from achievements import AchievementManager
from anime_data import search_anime, format_anime_message, load_animes, add_anime, delete_anime
from anime_search import search_anime_online

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Instance de la base de données
db = Database()

# Instance du gestionnaire d'accomplissements
achievement_manager = AchievementManager(db)

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
    if not update.effective_user:
        logger.error("Utilisateur non trouvé dans la commande start")
        return
        
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    
    # Enregistrer l'utilisateur dans la base de données
    db.register_user(user_id, user_name)
    
    # Vérifier l'éligibilité aux badges
    new_badges = achievement_manager.check_badge_eligibility(user_id)
    
    # Envoyer le message de bienvenue
    await update.message.reply_text(WELCOME_MESSAGE)
    
    # Si l'utilisateur a obtenu des badges, les notifier
    for badge in new_badges:
        await update.message.reply_text(
            BADGE_EARNED.format(
                emoji=badge['emoji'], 
                nom=badge['nom'], 
                description=badge['description']
            ),
            parse_mode='Markdown'
        )

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
    
    # Callbacks accessibles à tous les utilisateurs
    if query.data.startswith('anime:'):
        anime_id = int(query.data.replace('anime:', ''))
        results = context.user_data.get('anime_results', [])
        
        # Trouver l'anime dans les résultats
        anime = next((a for a in results if a['id'] == anime_id), None)
        
        if anime:
            message = format_anime_message(anime)
            await query.answer(f"Informations sur {anime['titre']}")
            
            # Envoyer les informations avec l'image de l'anime si disponible
            if anime.get('image'):
                # Répondre avec une nouvelle photo car edit_message_media n'est pas pratique ici
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=anime['image'],
                    caption=message,
                    parse_mode='HTML'
                )
                
                # Supprimer le message précédent pour éviter l'encombrement
                await query.message.delete()
            else:
                await query.message.edit_text(
                    message,
                    parse_mode='HTML'
                )
        else:
            await query.answer("Anime non trouvé.")
        return
    
    elif query.data == 'annuler_recherche':
        await query.answer("Recherche annulée")
        await query.message.edit_text(
            "Recherche annulée. Utilisez /anime pour faire une nouvelle recherche.",
            parse_mode='HTML'
        )
        return
    
    elif query.data == 'view_badges':
        profile_message = achievement_manager.format_user_progress(user_id)
        await query.answer("Affichage de vos badges")
        await query.message.edit_text(
            profile_message,
            parse_mode='Markdown',
            reply_markup=get_user_profile_keyboard()
        )
        return
        
    elif query.data == 'view_level':
        level_info = achievement_manager.get_user_level(user_id)
        message = f"📊 *Votre Niveau* 📊\n\n"
        message += f"{level_info['emoji']} Niveau: *{level_info['nom']}*\n"
        message += f"🔄 Points: *{level_info['points']}*"
        
        if level_info['prochain_niveau'] > level_info['niveau']:
            points_needed = level_info['points_prochain'] - level_info['points']
            message += f"\n\nIl vous manque *{points_needed} points* pour atteindre le niveau suivant."
        else:
            message += "\n\nFélicitations! Vous avez atteint le niveau maximum!"
        
        await query.answer("Affichage de votre niveau")
        await query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_user_profile_keyboard()
        )
        return
        
    elif query.data == 'view_leaderboard':
        leaderboard_message = achievement_manager.get_leaderboard()
        await query.answer("Affichage du classement")
        await query.message.edit_text(
            leaderboard_message,
            parse_mode='Markdown',
            reply_markup=get_user_profile_keyboard()
        )
        return
        
    elif query.data == 'share_bot':
        bot_info = await context.bot.get_me()
        bot_username = bot_info.username
        
        # Mettre à jour son activité (en comptant un partage)
        db.update_user_activity(user_id, share=True)
        
        # Vérifier l'éligibilité aux badges (pourrait avoir débloqué le badge ambassadeur)
        new_badges = achievement_manager.check_badge_eligibility(user_id)
        
        await query.answer("Merci de partager le bot!")
        await query.message.edit_text(
            SHARE_BOT_MESSAGE.format(bot_username=bot_username),
            parse_mode='Markdown',
            reply_markup=get_user_profile_keyboard()
        )
        
        # Si l'utilisateur a obtenu des badges, les notifier
        for badge in new_badges:
            await context.bot.send_message(
                chat_id=user_id,
                text=BADGE_EARNED.format(
                    emoji=badge['emoji'], 
                    nom=badge['nom'], 
                    description=badge['description']
                ),
                parse_mode='Markdown'
            )
        return
    
    # Pour les callbacks réservés aux admins, vérifier les permissions
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
        
    # Gestion des animes (admin)
    elif query.data == 'gerer_animes':
        await query.message.edit_text(
            "🎬 <b>Gestion des Animes</b>",
            parse_mode='HTML',
            reply_markup=get_anime_management_keyboard()
        )
        
    elif query.data == 'ajouter_anime':
        # Afficher le formulaire d'ajout d'anime
        await query.message.edit_text(
            ANIME_ADD_PROMPT,
            parse_mode='HTML'
        )
        context.user_data['state'] = 'attente_ajout_anime'
        
    elif query.data == 'supprimer_anime':
        # Afficher la liste des animes pour suppression
        animes = load_animes()
        if not animes:
            await query.message.edit_text(
                "❌ <b>Aucun anime disponible</b>\n\nLa base de données est vide.",
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
            return
            
        await query.message.edit_text(
            ANIME_DELETE_PROMPT,
            parse_mode='HTML',
            reply_markup=get_anime_list_keyboard(animes, 0, 10, True)
        )
        
    elif query.data == 'liste_animes':
        # Afficher la liste complète des animes
        animes = load_animes()
        
        if not animes:
            await query.message.edit_text(
                "❌ <b>Aucun anime disponible</b>\n\nLa base de données est vide.",
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
            return
            
        message = ANIME_LIST_HEADING.format(total=len(animes))
        
        await query.message.edit_text(
            message,
            parse_mode='HTML',
            reply_markup=get_anime_list_keyboard(animes, 0, 10, False)
        )
        
    elif query.data == 'rechercher_anime_admin':
        # Rediriger vers la commande /anime
        await query.message.edit_text(
            "🔍 <b>Recherche d'anime</b>\n\nUtilisez la commande /anime pour rechercher un anime.",
            parse_mode='HTML',
            reply_markup=get_anime_management_keyboard()
        )
        
    elif query.data.startswith('delete_anime:'):
        # Supprimer un anime
        anime_id = int(query.data.replace('delete_anime:', ''))
        success, message = delete_anime(anime_id)
        
        if success:
            # Récupérer le titre de l'anime depuis le message de retour
            title_match = re.search(r"'([^']+)'", message)
            title = title_match.group(1) if title_match else "l'anime"
            
            await query.message.edit_text(
                ANIME_DELETED_SUCCESS.format(titre=title),
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
        else:
            await query.message.edit_text(
                ANIME_DELETED_ERROR.format(error=message),
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
            
    elif query.data.startswith('view_anime:'):
        # Afficher les détails d'un anime
        anime_id = int(query.data.replace('view_anime:', ''))
        animes = load_animes()
        
        anime = next((a for a in animes if a['id'] == anime_id), None)
        
        if anime:
            message = format_anime_message(anime)
            
            if anime.get('image'):
                # Envoyer une nouvelle photo car edit_message_media est compliqué
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=anime['image'],
                    caption=message,
                    parse_mode='HTML'
                )
                
                # Supprimer le message précédent
                await query.message.delete()
            else:
                await query.message.edit_text(
                    message,
                    parse_mode='HTML',
                    reply_markup=get_anime_management_keyboard()
                )
        else:
            await query.message.edit_text(
                "❌ <b>Anime non trouvé</b>\n\nCet anime n'existe plus dans la base de données.",
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
            
    elif query.data.startswith('animes_page:'):
        # Gestion de la pagination pour les listes d'animes
        parts = query.data.split(':')
        if len(parts) < 3:
            return
        
        callback_prefix = parts[1]
        page = int(parts[2])
        for_deletion = callback_prefix == 'delete_anime'
        
        animes = load_animes()
        
        if not animes:
            await query.message.edit_text(
                "❌ <b>Aucun anime disponible</b>\n\nLa base de données est vide.",
                parse_mode='HTML',
                reply_markup=get_anime_management_keyboard()
            )
            return
            
        if for_deletion:
            message = ANIME_DELETE_PROMPT
        else:
            message = ANIME_LIST_HEADING.format(total=len(animes))
            
        await query.message.edit_text(
            message,
            parse_mode='HTML',
            reply_markup=get_anime_list_keyboard(animes, page, 10, for_deletion)
        )
        
    # Gestion des badges et accomplissements
    elif query.data == 'badges_settings':
        await query.message.edit_text(
            "🏆 Gestion des badges et accomplissements",
            reply_markup=get_badges_management_keyboard()
        )
        
    elif query.data == 'creer_badge':
        # Cette fonctionnalité sera développée ultérieurement
        await query.message.edit_text(
            "🚧 Cette fonctionnalité est en cours de développement.\n\n"
            "Elle permettra de créer des badges personnalisés pour les utilisateurs.",
            reply_markup=get_badges_management_keyboard()
        )
        
    elif query.data == 'attribuer_badge':
        # Récupérer la liste des utilisateurs pour l'attribution de badge
        users = db.get_all_users()
        
        if not users:
            await query.message.edit_text(
                "Aucun utilisateur enregistré pour le moment.",
                reply_markup=get_badges_management_keyboard()
            )
            return
            
        await query.message.edit_text(
            "Sélectionnez un utilisateur pour lui attribuer un badge:",
            reply_markup=get_user_selection_keyboard(users, 'select_user_badge')
        )
        
    elif query.data.startswith('select_user_badge:'):
        user_id = query.data.replace('select_user_badge:', '')
        context.user_data['selected_user_id'] = user_id
        
        user_data = db.get_user_data(user_id) or {}
        user_name = user_data.get('name', f"Utilisateur {user_id}")
        
        await query.message.edit_text(
            f"Sélectionnez un badge à attribuer à {user_name}:",
            reply_markup=get_award_badge_keyboard(achievements.BADGES)
        )
        
    elif query.data.startswith('award_badge:'):
        badge_id = query.data.replace('award_badge:', '')
        user_id = context.user_data.get('selected_user_id')
        
        if not user_id:
            await query.message.edit_text(
                "Erreur: Utilisateur non sélectionné.",
                reply_markup=get_badges_management_keyboard()
            )
            return
            
        # Attribuer le badge
        success = achievement_manager.award_badge(user_id, badge_id)
        
        if success:
            badge = achievements.BADGES[badge_id]
            user_data = db.get_user_data(user_id) or {}
            user_name = user_data.get('name', f"Utilisateur {user_id}")
            
            # Informer l'utilisateur qu'il a reçu un badge
            try:
                await context.bot.send_message(
                    chat_id=int(user_id),
                    text=BADGE_EARNED.format(
                        emoji=badge['emoji'],
                        nom=badge['nom'],
                        description=badge['description']
                    ),
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi de notification de badge à l'utilisateur {user_id}: {e}")
            
            await query.message.edit_text(
                f"✅ Badge {badge['emoji']} {badge['nom']} attribué avec succès à {user_name}!",
                reply_markup=get_badges_management_keyboard()
            )
        else:
            await query.message.edit_text(
                "❌ Erreur lors de l'attribution du badge ou l'utilisateur possède déjà ce badge.",
                reply_markup=get_badges_management_keyboard()
            )
            
    elif query.data == 'stats_badges':
        # Récupérer les statistiques de badges
        all_users = db.get_all_users()
        all_badges = []
        for user in all_users:
            all_badges.extend(user.get('badges', []))
        
        badge_counts = {}
        for badge in all_badges:
            badge_id = badge['id']
            if badge_id not in badge_counts:
                badge_counts[badge_id] = 0
            badge_counts[badge_id] += 1
        
        message = "📊 *Statistiques des Badges* 📊\n\n"
        
        # Total des badges attribués
        message += f"🏅 Total des badges attribués: *{len(all_badges)}*\n"
        message += f"👥 Utilisateurs avec au moins un badge: *{sum(1 for user in all_users if user.get('badges', []))}*\n\n"
        
        # Liste des badges par popularité
        message += "🏆 *Badges par popularité* 🏆\n"
        
        for badge_id, count in sorted(badge_counts.items(), key=lambda x: x[1], reverse=True):
            badge_info = achievements.BADGES.get(badge_id, {})
            emoji = badge_info.get('emoji', '🔶')
            nom = badge_info.get('nom', badge_id)
            message += f"{emoji} {nom}: *{count}* utilisateurs\n"
        
        if not badge_counts:
            message += "Aucun badge attribué pour le moment.\n"
        
        await query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_badges_management_keyboard()
        )
        
    elif query.data == 'stats' or query.data == 'stats_general':
        # Afficher les statistiques générales
        stats = db.get_stats()
        
        message = "📈 *Statistiques Globales* 📈\n\n"
        message += f"👥 Utilisateurs: *{stats.get('users_count', 0)}*\n"
        message += f"📺 Canaux actifs: *{stats.get('active_channels', 0)}*\n"
        message += f"📨 Messages traités: *{stats.get('total_messages', 0)}*\n"
        message += f"📢 Diffusions envoyées: *{stats.get('total_broadcasts', 0)}*\n\n"
        
        # Calcul des utilisateurs actifs
        all_users = db.get_all_users()
        active_users = 0
        
        for user in all_users:
            if 'last_seen' in user:
                try:
                    last_seen = datetime.fromisoformat(user['last_seen'])
                    now = datetime.now()
                    days_difference = (now - last_seen).days
                    
                    if days_difference < 7:  # Actif au cours des 7 derniers jours
                        active_users += 1
                except:
                    pass
        
        message += f"🔥 Utilisateurs actifs (7 jours): *{active_users}*\n"
        message += f"💯 Taux d'activité: *{int(active_users / stats.get('users_count', 1) * 100) if stats.get('users_count', 0) > 0 else 0}%*\n\n"
        
        # Formater la date de mise à jour
        last_update = "N/A"
        if 'last_update' in stats:
            try:
                last_update = datetime.fromisoformat(stats['last_update']).strftime('%d/%m/%Y %H:%M')
            except:
                last_update = stats['last_update']
        
        message += f"⏱ Dernière mise à jour: *{last_update}*"
        
        await query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_stats_keyboard()
        )
        
    elif query.data == 'stats_users':
        # Statistiques détaillées sur les utilisateurs
        all_users = db.get_all_users()
        
        message = "👥 *Statistiques des Utilisateurs* 👥\n\n"
        
        # Nombre total d'utilisateurs
        message += f"👤 Total des utilisateurs: *{len(all_users)}*\n\n"
        
        # Niveaux des utilisateurs
        levels = {}
        for user in all_users:
            level_info = achievement_manager.get_user_level(user['id'])
            level = level_info['niveau']
            if level not in levels:
                levels[level] = 0
            levels[level] += 1
        
        message += "📊 *Répartition par niveau* 📊\n"
        for level, count in sorted(levels.items()):
            level_data = achievements.NIVEAUX[level]
            percentage = int((count / len(all_users)) * 100) if all_users else 0
            message += f"{level_data['emoji']} {level_data['nom']}: *{count}* utilisateurs ({percentage}%)\n"
        
        # Statistiques d'activité
        message += "\n⏱ *Activité des utilisateurs* ⏱\n"
        active_24h = 0
        active_week = 0
        active_month = 0
        
        for user in all_users:
            if 'last_seen' in user:
                try:
                    last_seen = datetime.fromisoformat(user['last_seen'])
                    now = datetime.now()
                    days_difference = (now - last_seen).days
                    
                    if days_difference < 1:
                        active_24h += 1
                    if days_difference < 7:
                        active_week += 1
                    if days_difference < 30:
                        active_month += 1
                except:
                    pass
        
        message += f"🔥 Actifs (24h): *{active_24h}* ({int((active_24h / len(all_users)) * 100) if all_users else 0}%)\n"
        message += f"🔥 Actifs (7 jours): *{active_week}* ({int((active_week / len(all_users)) * 100) if all_users else 0}%)\n"
        message += f"🔥 Actifs (30 jours): *{active_month}* ({int((active_month / len(all_users)) * 100) if all_users else 0}%)\n"
        
        await query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_stats_keyboard()
        )
        
    elif query.data == 'stats_activity':
        # Statistiques détaillées sur l'activité du bot
        stats = db.get_stats()
        
        message = "📈 *Activité du Bot* 📈\n\n"
        
        # Données générales d'utilisation
        message += f"📤 Messages envoyés: *{stats.get('total_messages', 0)}*\n"
        message += f"📢 Diffusions: *{stats.get('total_broadcasts', 0)}*\n"
        message += f"📺 Canaux actifs: *{stats.get('active_channels', 0)}*\n\n"
        
        # Calculer la moyenne quotidienne de diffusions
        now = datetime.now()
        days_running = (now - datetime.fromisoformat(stats.get('start_date', now.isoformat()))).days or 1
        avg_broadcasts = round(stats.get('total_broadcasts', 0) / max(days_running, 1), 2)
        
        message += f"📊 Diffusions par jour (moyenne): *{avg_broadcasts}*\n"
        message += f"⏱ Jours d'activité: *{days_running}*\n\n"
        
        # Date de dernière mise à jour des statistiques
        last_update = "N/A"
        if 'last_update' in stats:
            try:
                last_update = datetime.fromisoformat(stats['last_update']).strftime('%d/%m/%Y %H:%M')
            except:
                last_update = stats['last_update']
        
        message += f"⏱ Dernière mise à jour: *{last_update}*"
        
        await query.message.edit_text(
            message,
            parse_mode='Markdown',
            reply_markup=get_stats_keyboard()
        )
        
    elif query.data.startswith('page:'):
        # Gestion de la pagination pour les listes d'utilisateurs
        parts = query.data.split(':')
        if len(parts) < 3:
            return
        
        callback_prefix = parts[1]
        page = int(parts[2])
        
        if callback_prefix == 'select_user_badge':
            users = db.get_all_users()
            
            if not users:
                await query.message.edit_text(
                    "Aucun utilisateur enregistré pour le moment.",
                    reply_markup=get_badges_management_keyboard()
                )
                return
                
            await query.message.edit_text(
                "Sélectionnez un utilisateur pour lui attribuer un badge:",
                reply_markup=get_user_selection_keyboard(users, 'select_user_badge', page)
            )

async def process_anime_search(update: Update, context: ContextTypes.DEFAULT_TYPE, anime_name: str):
    """Traite une recherche d'anime et affiche les résultats"""
    # D'abord rechercher dans la base de données locale
    # Limiter à 10 résultats pour éviter un menu trop long
    results = search_anime(anime_name, limit=10)
    
    # Si aucun résultat local, rechercher en ligne via l'API Jikan (MyAnimeList)
    if not results:
        # Informer l'utilisateur que la recherche se poursuit en ligne
        waiting_message = await update.message.reply_text(
            "🔄 <b>Recherche en ligne...</b>\n\nAucun résultat trouvé localement. Recherche étendue en cours...",
            parse_mode='HTML'
        )
        
        # Rechercher via l'API en ligne
        online_results = search_anime_online(anime_name, limit=10)
        
        if online_results:
            # Si des résultats sont trouvés en ligne, les utiliser
            results = online_results
            await waiting_message.delete()
        else:
            # Si toujours aucun résultat, informer l'utilisateur
            await waiting_message.edit_text(
                ANIME_NOT_FOUND,
                parse_mode='HTML'
            )
            return
    
    if len(results) == 1:
        # Un seul résultat trouvé, afficher directement
        anime = results[0]
        message = format_anime_message(anime)
        
        # Indiquer si le résultat vient de la base de données locale ou de l'API
        source_info = "\n\n<i>Source: Base de données locale</i>"
        if anime.get('source') == 'api':
            source_info = "\n\n<i>Source: MyAnimeList (via API)</i>"
        
        message += source_info
        
        # Envoyer les informations avec l'image de l'anime
        if anime.get('image'):
            try:
                await update.message.reply_photo(
                    photo=anime['image'],
                    caption=message,
                    parse_mode='HTML'
                )
            except Exception as e:
                logging.error(f"Erreur lors de l'envoi de l'image: {e}")
                await update.message.reply_text(
                    message + "\n\n<i>⚠️ L'image n'a pas pu être affichée</i>",
                    parse_mode='HTML'
                )
        else:
            await update.message.reply_text(
                message,
                parse_mode='HTML'
            )
    else:
        # Si la recherche exacte ne donne qu'un seul résultat vraiment pertinent
        # (cas où un anime commence exactement par la recherche, mais d'autres contiennent le terme)
        exact_matches = [anime for anime in results if anime['titre'].lower().startswith(anime_name.lower())]
        if len(exact_matches) == 1 and len(anime_name) > 3:  # Au moins 4 caractères pour éviter les faux positifs
            anime = exact_matches[0]
            message = format_anime_message(anime)
            
            # Indiquer si le résultat vient de la base de données locale ou de l'API
            source_info = "\n\n<i>Source: Base de données locale</i>"
            if anime.get('source') == 'api':
                source_info = "\n\n<i>Source: MyAnimeList (via API)</i>"
            
            message += source_info
            
            # Envoyer les informations avec l'image de l'anime
            if anime.get('image'):
                try:
                    await update.message.reply_photo(
                        photo=anime['image'],
                        caption=message,
                        parse_mode='HTML'
                    )
                except Exception as e:
                    logging.error(f"Erreur lors de l'envoi de l'image: {e}")
                    await update.message.reply_text(
                        message + "\n\n<i>⚠️ L'image n'a pas pu être affichée</i>",
                        parse_mode='HTML'
                    )
            else:
                await update.message.reply_text(
                    message,
                    parse_mode='HTML'
                )
        else:
            # Plusieurs résultats trouvés, proposer un choix
            source_message = ""
            if any(anime.get('source') == 'api' for anime in results):
                source_message = "\n\n<i>La recherche inclut des résultats depuis MyAnimeList</i>"
                
            message = ANIME_MULTIPLE_RESULTS + source_message
            for i, anime in enumerate(results, 1):
                source_tag = " 🌐" if anime.get('source') == 'api' else ""
                message += f"\n{i}. {anime['titre']}{source_tag}"
                
            # Stocker les résultats pour une utilisation ultérieure
            context.user_data['anime_results'] = results
            
            # Ajouter un bouton pour continuer la recherche en ligne si tous les résultats sont locaux
            if not any(anime.get('source') == 'api' for anime in results):
                await update.message.reply_text(
                    message,
                    parse_mode='HTML',
                    reply_markup=get_anime_selection_keyboard(results, online_search=True)
                )
            else:
                await update.message.reply_text(
                    message,
                    parse_mode='HTML',
                    reply_markup=get_anime_selection_keyboard(results)
                )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages reçus"""
    if not update or not update.effective_user:
        logger.error("Utilisateur non trouvé dans le message")
        return

    user_id = update.effective_user.id
    state = context.user_data.get('state')
    
    # Gestion de la recherche d'anime par nom
    if state == 'attente_nom_anime':
        anime_name = update.message.text
        if anime_name and not anime_name.startswith('/'):
            await process_anime_search(update, context, anime_name)
            context.user_data.pop('state', None)
            return
            
    # Si l'utilisateur n'est pas admin, ne pas traiter les autres états
    if not db.is_admin(user_id):
        return
        
    # Gestion de l'ajout d'anime (admin uniquement)
    if state == 'attente_ajout_anime':
        anime_text = update.message.text
        if not anime_text:
            await update.message.reply_text(
                "❌ <b>Format invalide</b>\n\nVeuillez envoyer les informations de l'anime selon le format demandé.",
                parse_mode='HTML'
            )
            return
            
        # Parser les données de l'anime
        anime_data = {}
        lines = anime_text.split('\n')
        
        for line in lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                
                if key == 'titre':
                    anime_data['titre'] = value
                elif key == 'titre japonais':
                    anime_data['titre_japonais'] = value
                elif key == 'image':
                    anime_data['image'] = value
                elif key == 'synopsis':
                    anime_data['synopsis'] = value
                elif key == 'date début':
                    anime_data['date_debut'] = value
                elif key == 'date fin':
                    anime_data['date_fin'] = value
                elif key == 'épisodes' or key == 'episodes':
                    try:
                        anime_data['episodes'] = int(value)
                    except ValueError:
                        anime_data['episodes'] = value
                elif key == 'durée' or key == 'duree':
                    anime_data['duree'] = value
                elif key == 'status':
                    anime_data['status'] = value
                elif key == 'score':
                    try:
                        anime_data['score'] = float(value)
                    except ValueError:
                        anime_data['score'] = 0.0
                elif key == 'genres':
                    anime_data['genres'] = [g.strip() for g in value.split(',')]
                elif key == 'studios':
                    anime_data['studios'] = [s.strip() for s in value.split(',')]
        
        # Ajouter l'anime à la base de données
        success, message = add_anime(anime_data)
        
        if success:
            await update.message.reply_text(
                ANIME_ADDED_SUCCESS.format(titre=anime_data['titre']),
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                ANIME_ADDED_ERROR.format(error=message),
                parse_mode='HTML'
            )
            
        context.user_data.pop('state', None)
        return

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
        
    elif state == 'attente_nom_anime':
        anime_name = update.message.text
        await process_anime_search(update, context, anime_name)
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
        
    if update.effective_user:
        # Enregistrer l'utilisateur s'il n'existe pas déjà
        db.register_user(update.effective_user.id, update.effective_user.full_name)
        # Mettre à jour son activité
        db.update_user_activity(update.effective_user.id, message=True)
        
    await update.message.reply_text(HELP_MESSAGE)



async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /anime pour rechercher des informations sur un anime"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans anime_command")
        return
        
    # Si aucun argument n'est fourni, demander un nom d'anime
    args = context.args
    if not args:
        await update.message.reply_text(
            ANIME_SEARCH_PROMPT,
            parse_mode='HTML'
        )
        context.user_data['state'] = 'attente_nom_anime'
        return
        
    # Joindre tous les arguments pour former le nom de l'anime
    anime_name = ' '.join(args)
    await process_anime_search(update, context, anime_name)
    
async def addanime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /addanime pour ajouter un nouvel anime"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans addanime_command")
        return
    
    # Vérifier que l'utilisateur est admin
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text(NOT_ADMIN)
        return
        
    # Si la commande contient du texte sous forme de caption, l'utiliser comme données
    text = update.message.text
    
    # Supprimer "/addanime" du texte
    if text.startswith('/addanime'):
        text = text[len('/addanime'):].strip()
    
    if text:
        # Parser le texte comme données d'anime
        anime_data = {}
        lines = text.split('\n')
        
        for line in lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip().lower()
                value = parts[1].strip()
                
                if key == 'titre':
                    anime_data['titre'] = value
                elif key == 'titre japonais':
                    anime_data['titre_japonais'] = value
                elif key == 'image':
                    anime_data['image'] = value
                elif key == 'synopsis':
                    anime_data['synopsis'] = value
                elif key == 'date début':
                    anime_data['date_debut'] = value
                elif key == 'date fin':
                    anime_data['date_fin'] = value
                elif key == 'épisodes' or key == 'episodes':
                    try:
                        anime_data['episodes'] = int(value)
                    except ValueError:
                        anime_data['episodes'] = value
                elif key == 'durée' or key == 'duree':
                    anime_data['duree'] = value
                elif key == 'status':
                    anime_data['status'] = value
                elif key == 'score':
                    try:
                        anime_data['score'] = float(value)
                    except ValueError:
                        anime_data['score'] = 0.0
                elif key == 'genres':
                    anime_data['genres'] = [g.strip() for g in value.split(',')]
                elif key == 'studios':
                    anime_data['studios'] = [s.strip() for s in value.split(',')]
        
        # Vérifier si les données sont complètes
        if anime_data:
            # Ajouter l'anime à la base de données
            success, message = add_anime(anime_data)
            
            if success:
                await update.message.reply_text(
                    ANIME_ADDED_SUCCESS.format(titre=anime_data['titre']),
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(
                    ANIME_ADDED_ERROR.format(error=message),
                    parse_mode='HTML'
                )
        else:
            # Si aucune donnée n'a été trouvée, afficher l'aide
            await update.message.reply_text(
                ANIME_ADMIN_HELP,
                parse_mode='HTML'
            )
    else:
        # Si la commande est vide, afficher le formulaire
        await update.message.reply_text(
            ANIME_ADD_PROMPT,
            parse_mode='HTML'
        )
        context.user_data['state'] = 'attente_ajout_anime'
        
async def deleteanime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /deleteanime pour supprimer un anime"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans deleteanime_command")
        return
    
    # Vérifier que l'utilisateur est admin
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text(NOT_ADMIN)
        return
    
    # Si un ID est fourni, supprimer directement
    args = context.args
    if args:
        try:
            anime_id = int(args[0])
            success, message = delete_anime(anime_id)
            
            if success:
                # Récupérer le titre de l'anime depuis le message de retour
                title_match = re.search(r"'([^']+)'", message)
                title = title_match.group(1) if title_match else "l'anime"
                
                await update.message.reply_text(
                    ANIME_DELETED_SUCCESS.format(titre=title),
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(
                    ANIME_DELETED_ERROR.format(error=message),
                    parse_mode='HTML'
                )
        except ValueError:
            await update.message.reply_text(
                "❌ <b>ID invalide</b>\n\nL'ID doit être un nombre entier.",
                parse_mode='HTML'
            )
    else:
        # Afficher la liste des animes pour suppression
        animes = load_animes()
        if not animes:
            await update.message.reply_text(
                "❌ <b>Aucun anime disponible</b>\n\nLa base de données est vide.",
                parse_mode='HTML'
            )
            return
            
        await update.message.reply_text(
            ANIME_DELETE_PROMPT,
            parse_mode='HTML',
            reply_markup=get_anime_list_keyboard(animes, 0, 10, True)
        )
        
async def listanimes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /listanimes pour afficher la liste des animes"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans listanimes_command")
        return
    
    # Vérifier que l'utilisateur est admin
    user_id = update.effective_user.id
    if not db.is_admin(user_id):
        await update.message.reply_text(NOT_ADMIN)
        return
    
    # Afficher la liste des animes
    animes = load_animes()
    
    if not animes:
        await update.message.reply_text(
            "❌ <b>Aucun anime disponible</b>\n\nLa base de données est vide.",
            parse_mode='HTML'
        )
        return
        
    message = ANIME_LIST_HEADING.format(total=len(animes))
    
    await update.message.reply_text(
        message,
        parse_mode='HTML',
        reply_markup=get_anime_list_keyboard(animes, 0, 10, False)
    )
    
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /stats - Affiche les statistiques publiques du bot"""
    if not update or not update.message:
        logger.error("Message invalide reçu dans stats_command")
        return
    
    if update.effective_user:
        # Enregistrer l'utilisateur s'il n'existe pas déjà
        db.register_user(update.effective_user.id, update.effective_user.full_name)
        db.update_user_activity(update.effective_user.id, message=True)
    
    # Récupérer les statistiques
    stats = db.get_stats()
    
    # Récupérer les utilisateurs les mieux classés
    top_users = sorted(db.get_all_users(), key=lambda u: u.get('points', 0), reverse=True)[:3]
    top_users_text = ""
    for i, user in enumerate(top_users, 1):
        level_info = achievement_manager.get_user_level(user['id'])
        user_name = user.get('name', f"Utilisateur {user['id']}")
        top_users_text += f"{i}. {level_info['emoji']} {user_name}: {user.get('points', 0)} points\n"
    
    if not top_users_text:
        top_users_text = "Aucun utilisateur classé pour le moment."
    
    # Calculer les badges les plus populaires
    all_badges = []
    for user in db.get_all_users():
        all_badges.extend(user.get('badges', []))
    
    badge_counts = {}
    for badge in all_badges:
        badge_id = badge['id']
        if badge_id not in badge_counts:
            badge_counts[badge_id] = 0
        badge_counts[badge_id] += 1
    
    # Obtenir les 3 badges les plus populaires
    popular_badges_text = ""
    for badge_id, count in sorted(badge_counts.items(), key=lambda x: x[1], reverse=True)[:3]:
        badge_info = next((b for b in all_badges if b['id'] == badge_id), None)
        if badge_info:
            popular_badges_text += f"{badge_info['emoji']} {badge_info['nom']}: {count} utilisateurs\n"
    
    if not popular_badges_text:
        popular_badges_text = "Aucun badge attribué pour le moment."
    
    # Formater la date de mise à jour
    last_update = "N/A"
    if 'last_update' in stats:
        try:
            last_update = datetime.fromisoformat(stats['last_update']).strftime('%d/%m/%Y %H:%M')
        except:
            last_update = stats['last_update']
    
    # Envoyer les statistiques
    await update.message.reply_text(
        STATS_MESSAGE.format(
            users_count=stats.get('users_count', 0),
            active_channels=stats.get('active_channels', 0),
            total_messages=stats.get('total_messages', 0),
            total_broadcasts=stats.get('total_broadcasts', 0),
            last_update=last_update,
            top_users=top_users_text,
            popular_badges=popular_badges_text
        ),
        parse_mode='Markdown'
    )

async def share_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /share - Offre un moyen de partager le bot"""
    if not update or not update.message or not update.effective_user:
        logger.error("Utilisateur non trouvé dans la commande share")
        return
    
    user_id = update.effective_user.id
    
    # Enregistrer l'utilisateur s'il n'existe pas déjà
    db.register_user(user_id, update.effective_user.full_name)
    
    # Mettre à jour son activité (en comptant un partage)
    db.update_user_activity(user_id, message=True, share=True)
    
    # Vérifier l'éligibilité aux badges (pourrait avoir débloqué le badge ambassadeur)
    new_badges = achievement_manager.check_badge_eligibility(user_id)
    
    # Obtenir le nom d'utilisateur du bot
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username
    
    # Envoyer le message de partage
    await update.message.reply_text(
        SHARE_BOT_MESSAGE.format(bot_username=bot_username),
        parse_mode='Markdown'
    )
    
    # Si l'utilisateur a obtenu des badges, les notifier
    for badge in new_badges:
        await update.message.reply_text(
            BADGE_EARNED.format(
                emoji=badge['emoji'], 
                nom=badge['nom'], 
                description=badge['description']
            ),
            parse_mode='Markdown'
        )