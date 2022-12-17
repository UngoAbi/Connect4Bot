import json
import random
import discord
from discord.ext import commands
from Connect4Bot.utils import create_embed


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'game' command is loaded")

    @commands.command()
    async def game(self, context, game_id):
        pass


def generate_game_id():
    with open("connect4/games.json", "w") as file:
        json_file = json.load(file)
        game_id = random.random()[-4:]
        while id in json_file:
            game_id = random.random()[-4:]

        json_file[game_id] = {
            "state": [["0" for _ in range(7)] for _ in range(6)],
            "turn": "1"
        }
        file.write(json_file)
    return game_id


async def setup(bot):
    await bot.add_cog(Game(bot))
