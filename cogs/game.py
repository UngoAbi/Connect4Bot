import json
import random
import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot.utils import create_embed, numbers
from Connect4Bot import c4game


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'game' command is loaded")

    @commands.command()
    async def game(self, context, game_id):
        with open("games.json") as file:
            json_file = json.load(file)

        if game_id not in json_file:
            embed = create_embed(
                title="Error",
                description="This game doesn't exist",
                color=discord.Color.red()
            )
            context.send(embed=embed)

        elif json_file.get(game_id).get("on_going"):
            await self.play(context, game_id)

        else:
            await self.watch(context, game_id)

    async def play(self, context, game_id):
        with open("games.json") as file:
            json_file = json.load(file)
        data = json_file.get(game_id)

        embed = create_embed(
            title=c4game.get_title(self.bot, data, game_id),
            description=c4game.get_grid(data),
            color=discord.Color.blue()
        )
        view = View()
        for number in range(7):
            view.add_item(self.get_number_button(json_file, game_id, number))

        try:
            await context.send(embed=embed, view=view)
        except AttributeError:
            await context.response.edit_message(embed=embed, view=view)

    async def watch(self, context, game_id):
        pass

    def get_number_button(self, json_file, game_id, number):
        async def callback(interaction):
            if c4game.insert_chip(json_file.get(game_id), number) == False:
                return

            with open("games.json", "w") as file:
                json.dump(json_file, file, indent=2)

            await self.game(interaction, game_id)

        button = Button(emoji=numbers[number])
        button.callback = callback
        return button


def generate_game_id(players):
    with open("games.json") as file:
        json_file = json.load(file)

    players = [player.id for player in random.sample(players, k=2)]
    game_id = str(random.random())[-4:]
    while game_id in json_file:
        game_id = random.random()[-4:]

    json_file[game_id] = {
        "state": [["0" for _ in range(7)] for _ in range(6)],
        "players": players,
        "moves": [],
        "on_going": True
    }

    with open("games.json", "w") as file:
        json.dump(json_file, file, indent=2)
    return game_id


async def setup(bot):
    await bot.add_cog(Game(bot))
