
# 🎮 Bot Discord – Jeux en commun

## 🚀 Déploiement rapide

1. Crée un bot sur https://discord.com/developers/applications
2. Active :
   - Bot
   - Privileged Gateway Intents → Server Members
3. Copie le TOKEN

## ▶️ Lancer le bot en local
```bash
pip install -r requirements.txt
export BOT_TOKEN=ton_token
python bot.py
```

## 🌍 Hébergement gratuit (Railway)
- Crée un projet Railway
- Déploie depuis GitHub ou upload ce dossier
- Ajoute la variable BOT_TOKEN

## 📘 Commandes Slash
- /addjeu
- /removejeu
- /mesjeux
- /setjeux
- /jeu pseudo1;pseudo2
