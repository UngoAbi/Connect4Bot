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
        with open("connect4/games.json") as file:
            json_file = json.load(file)
        game_is_on_going = json_file.get(game_id).get("on_going")

        if game_id not in json_file:
            embed = create_embed(
                title="Error",
                description="This game doesn't exist",
                color=discord.Color.red()
            )
            context.send(embed=embed)

        elif not game_is_on_going:
            await self.watch(context, game_id)

        else:
            await self.play(context, game_id)

    async def watch(self, context, game_id):
        pass

    async def play(self, context, game_id):
        pass


def generate_game_id(players):
    with open("connect4/games.json") as file:
        json_file = json.load(file)

    game_id = str(random.random())[-4:]
    while game_id in json_file:
        game_id = random.random()[-4:]
    players = random.sample(players, k=2)
    json_file[game_id] = {
        "state": [["0" for _ in range(7)] for _ in range(6)],
        "player1": players[0],
        "player2": players[1],
        "turn": 1,
        "on_going": True,
        "moves": []
    }

    with open("connect4/games.json", "w") as file:
        json.dump(json_file, file, indent=2)

    return game_id


async def setup(bot):
    await bot.add_cog(Game(bot))
