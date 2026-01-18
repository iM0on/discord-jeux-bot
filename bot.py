import discord
from discord import app_commands
import os
import json

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

DATA_FILE = "data.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

@tree.command(name="addjeu", description="Add a game to your library")
async def addjeu(interaction: discord.Interaction, game: str):
    data = load_data()
    uid = str(interaction.user.id)
    data.setdefault(uid, [])
    if game not in data[uid]:
        data[uid].append(game)
        save_data(data)
    await interaction.response.send_message(f"✅ Jeu ajouté : {game}", ephemeral=True)

@tree.command(name="mesjeux", description="Show your games")
async def mesjeux(interaction: discord.Interaction):
    data = load_data()
    games = data.get(str(interaction.user.id), [])
    if not games:
        await interaction.response.send_message("❌ Aucun jeu enregistré.", ephemeral=True)
    else:
        await interaction.response.send_message(
            "🎮 Tes jeux :\n" + "\n".join(games),
            ephemeral=True
        )

@tree.command(name="play", description="Common games with your voice channel")
async def play(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message(
            "❌ Tu dois être dans un salon vocal.",
            ephemeral=True
        )
        return

    channel = interaction.user.voice.channel
    data = load_data()

    members = [m for m in channel.members if not m.bot]
    if len(members) < 2:
        await interaction.response.send_message(
            "❌ Pas assez de joueurs dans le vocal.",
            ephemeral=True
        )
        return

    common = None
    for m in members:
        games = set(data.get(str(m.id), []))
        common = games if common is None else common & games

    if not common:
        await interaction.response.send_message("😅 Aucun jeu en commun.", ephemeral=True)
    else:
        await interaction.response.send_message(
            f"🎧 Jeux en commun ({len(members)} joueurs) :\n" + "\n".join(common)
        )

client.run(TOKEN)
