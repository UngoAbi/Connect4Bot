import json
import discord
from discord.ext import commands


with open("token.json") as f:
    TOKEN = json.load(f)["TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    owner_id=449638484597276672
)


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print("Beep Boop")


bot.run(TOKEN)
