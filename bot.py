import os
import asyncio
import discord
from discord.ext import commands
from consts import *


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    owner_id=OWNER_ID,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"[INIT] name: {bot.user.name}")
    print(f"[INIT] id: {bot.user.id}")
    print("[INIT] beep boop")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())