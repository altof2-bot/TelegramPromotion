# Bot Telegram pour la Promotion de Canaux

Ce projet est un bot Telegram en français pour la promotion de canaux avec un panneau d'administration.

## Fonctionnalités
- Panneau admin avec clavier inline pour faciliter la gestion
- Diffusion de contenu (texte, images, vidéos, stickers)
- Gestion des canaux (ajout, suppression, listage)
- Gestion des administrateurs
- Vérification du statut d'admin du bot dans les canaux
- Support pour la commande /addchannel par les utilisateurs

## Déploiement sur Koyeb

### Prérequis
- Un compte Koyeb
- Un token de bot Telegram (obtenu via @BotFather)

### Étapes de déploiement

1. Créez une nouvelle application sur Koyeb
2. Configurez le déploiement avec les paramètres suivants:
   - **Source**: GitHub (ou autre dépôt)
   - **Repository**: URL de ce dépôt
   - **Branch**: main (ou votre branche principale)
   - **Build mode**: Buildpacks
   - **Name**: anime-promotion-bot (ou un autre nom)

3. Ajoutez les variables d'environnement:
   - `TELEGRAM_BOT_TOKEN`: Votre token de bot Telegram (actuellement `7834676836:AAHCHXoZerNO_IDIwiz3WrpbFHbMbnTS2HQ`)

4. Configurez les ressources:
   - **Instance Type**: Minimal (ou supérieur selon vos besoins)
   - **Scaling**: Min: 1, Max: 1

5. Validez et déployez

### Fichiers de configuration
- `Procfile`: Configure les processus pour Koyeb
  - `web`: Serveur web Flask pour maintenir l'application active
  - `worker`: Le bot Telegram lui-même
- `requirements-koyeb.txt`: Liste des dépendances

### Surveillance et maintenance
- Configurez UptimeRobot pour pinger l'endpoint `/ping` afin d'assurer une activité 24/7
- Vous pouvez vérifier l'état du bot à tout moment en visitant l'URL de l'application Koyeb

## Tarifs d'abonnement
- 10 étoiles → 3 jours
- 15 étoiles → 1 semaine
- 25 étoiles → 1 mois
- 50 étoiles → 2 mois

## Contact et support
Pour toute question ou assistance, contactez @altof2 sur Telegram.