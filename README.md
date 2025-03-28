# Bot Telegram pour la Promotion de Canaux

Ce bot Telegram en français est conçu pour aider à la promotion de canaux d'anime avec un panneau d'administration complet.

## Fonctionnalités

- Panneau administrateur avec clavier inline
- Diffusion de contenu (texte, images, vidéos, stickers)
- Gestion des canaux (ajout, suppression, listage)
- Gestion des administrateurs
- Vérification du statut d'admin du bot dans les canaux
- Support pour la commande /addchannel par les utilisateurs

## Configuration

1. Obtenez un token de bot Telegram via [@BotFather](https://t.me/BotFather)
2. Ajoutez votre token dans les secrets d'environnement: `TELEGRAM_BOT_TOKEN`

## Démarrage Local

```bash
# Démarrer le serveur Flask (pour maintenir le bot actif via UptimeRobot)
python app.py

# Dans un autre terminal, démarrez le bot
python app.py bot
```

## Commandes Disponibles

- `/start` - Démarrer le bot et voir le message d'accueil
- `/help` - Afficher l'aide
- `/admin` - Accéder au panneau d'administration (seulement pour les admins)
- `/addchannel` - Ajouter un canal (format: @username ou -100xxx)

## Tarifs d'abonnement

- 10 étoiles → 3 jours
- 15 étoiles → 1 semaine
- 25 étoiles → 1 mois
- 50 étoiles → 2 mois

## Déploiement sur Koyeb

Voir le fichier [README-koyeb.md](README-koyeb.md) pour les instructions détaillées de déploiement.

## Contact et Support

Pour toute question ou assistance, contactez @altof2 sur Telegram.