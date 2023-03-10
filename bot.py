import os
import asyncio
import discord
from discord.ext import commands
from utils import token, owner_id


intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="$",
    intents=intents,
    owner_id=owner_id,
    help_command=None
)


@bot.event
async def on_ready() -> None:
    print(f"[INIT] name: {bot.user.name}")
    print(f"[INIT] id: {bot.user.id}")
    print("[INIT] beep boop")


async def load() -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main() -> None:
    await load()
    await bot.start(token)


asyncio.run(main())
