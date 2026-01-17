
import os
import discord
from discord import app_commands
import sqlite3

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

db = sqlite3.connect("database.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    guild_id INTEGER,
    user_id INTEGER,
    game TEXT
)
""")
db.commit()

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot connecté en tant que {client.user}")

@tree.command(name="addjeu", description="Ajouter un jeu à ta liste")
async def addjeu(interaction: discord.Interaction, jeu: str):
    cursor.execute(
        "INSERT INTO games VALUES (?, ?, ?)",
        (interaction.guild.id, interaction.user.id, jeu.lower())
    )
    db.commit()
    await interaction.response.send_message(f"🎮 {jeu} ajouté")

@tree.command(name="removejeu", description="Supprimer un jeu")
async def removejeu(interaction: discord.Interaction, jeu: str):
    cursor.execute(
        "DELETE FROM games WHERE guild_id=? AND user_id=? AND game=?",
        (interaction.guild.id, interaction.user.id, jeu.lower())
    )
    db.commit()
    await interaction.response.send_message(f"❌ {jeu} supprimé")

@tree.command(name="mesjeux", description="Voir ta liste de jeux")
async def mesjeux(interaction: discord.Interaction):
    cursor.execute(
        "SELECT game FROM games WHERE guild_id=? AND user_id=?",
        (interaction.guild.id, interaction.user.id)
    )
    games = [g[0] for g in cursor.fetchall()]
    if games:
        await interaction.response.send_message("🎮 Tes jeux:\n" + "\n".join(games))
    else:
        await interaction.response.send_message("❌ Aucun jeu enregistré")

@tree.command(name="setjeux", description="Définir toute ta liste de jeux")
async def setjeux(interaction: discord.Interaction, jeux: str):
    cursor.execute(
        "DELETE FROM games WHERE guild_id=? AND user_id=?",
        (interaction.guild.id, interaction.user.id)
    )
    for game in jeux.split(","):
        cursor.execute(
            "INSERT INTO games VALUES (?, ?, ?)",
            (interaction.guild.id, interaction.user.id, game.strip().lower())
        )
    db.commit()
    await interaction.response.send_message("✅ Liste mise à jour")

@tree.command(name="jeu", description="Voir les jeux en commun")
async def jeu(interaction: discord.Interaction, pseudos: str):
    pseudos = pseudos.split(";")
    members = []
    for p in pseudos:
        m = discord.utils.find(lambda m: m.name == p, interaction.guild.members)
        if not m:
            await interaction.response.send_message(f"❌ Utilisateur introuvable : {p}")
            return
        members.append(m.id)

    common = None
    for uid in members:
        cursor.execute(
            "SELECT game FROM games WHERE guild_id=? AND user_id=?",
            (interaction.guild.id, uid)
        )
        games = {g[0] for g in cursor.fetchall()}
        common = games if common is None else common & games

    if common:
        await interaction.response.send_message("🎮 Jeux en commun:\n" + "\n".join(common))
    else:
        await interaction.response.send_message("❌ Aucun jeu en commun")

client.run(TOKEN)
