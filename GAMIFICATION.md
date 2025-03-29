# Guide de Gamification pour le Bot Telegram

Ce document explique les fonctionnalités de gamification implémentées dans le bot Telegram de diffusion d'animes.

## 🏆 Système de badges et niveaux

Le bot intègre un système de gamification complet qui permet aux utilisateurs de gagner des points, débloquer des badges et monter en niveau au fur et à mesure de leur interaction avec le bot.

### Badges disponibles

| Badge | Nom | Description | Points accordés |
|-------|-----|-------------|----------------|
| 🔰 | Nouveau Membre | Rejoint le bot de publication anime | 5 |
| 🌟 | Abonné | S'est abonné à un canal anime | 10 |
| 📢 | Ambassadeur | A partagé le bot avec d'autres utilisateurs | 15 |
| 🏆 | Utilisateur Fidèle | Utilise le bot depuis plus d'une semaine | 20 |
| 💎 | Membre Premium | A souscrit à un abonnement premium | 30 |

### Niveaux

Les utilisateurs accumulent des points en obtenant des badges et peuvent monter dans les niveaux suivants :

| Niveau | Nom | Points requis |
|--------|-----|---------------|
| 0 | 🥉 Débutant | 0 |
| 1 | 🥈 Régulier | 20 |
| 2 | 🥇 Passionné | 50 |
| 3 | 🏅 Expert | 100 |
| 4 | 👑 Légende | 200 |

## 📋 Commandes utilisateur

Les commandes suivantes sont disponibles pour tous les utilisateurs :

- `/stats` - Affiche les statistiques publiques du bot
- `/share` - Génère un lien de partage pour inviter d'autres utilisateurs

## 🎮 Interface utilisateur

L'interface utilisateur du bot a été améliorée avec des boutons interactifs qui permettent une navigation intuitive. Les profils utilisateurs et le classement sont accessibles uniquement via le panneau d'administration pour les administrateurs du bot.

### Statistiques

Les statistiques publiques incluent :
- Nombre total d'utilisateurs
- Nombre de canaux actifs
- Nombre total de messages traités
- Nombre de diffusions envoyées
- Les utilisateurs de premier plan
- Les badges les plus populaires

## 🛠️ Administration des badges

Les administrateurs peuvent gérer les badges des utilisateurs :

- Attribuer des badges manuellement
- Consulter les statistiques détaillées des badges
- Voir quels badges sont les plus populaires

Pour accéder au panneau d'administration des badges, les administrateurs peuvent utiliser la commande `/admin` puis sélectionner "🏆 Badges & Niveaux".

## 🤖 Attribution automatique des badges

Certains badges sont attribués automatiquement :

- 🔰 **Nouveau Membre** - Attribué lors de la première interaction avec le bot
- 🏆 **Utilisateur Fidèle** - Attribué après une semaine d'utilisation du bot
- 📢 **Ambassadeur** - Attribué lorsque l'utilisateur partage le bot

Les autres badges peuvent être attribués manuellement par les administrateurs ou automatiquement lors d'événements spécifiques.

---

Pour toute question ou suggestion concernant le système de gamification, contactez l'administrateur du bot.