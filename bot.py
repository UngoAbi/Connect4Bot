import os
import asyncio
import discord
from discord.ext import commands
from constants import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    owner_id=449638484597276672,
    help_command=None
)


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)
    print("Beep Boop")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
