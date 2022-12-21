import json
import random
import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot import utils


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'game' command is loaded")

    @commands.command()
    async def game(self, context, game_id):
        with open("games.json") as outfile:
            json_file = json.load(outfile)

        if game_id not in json_file:
            await self.error_game_not_found(context)
        elif json_file.get(game_id).get("on_going"):
            await self.play(context, game_id)
        else:
            await self.replay(context, game_id)

    async def play(self, context, game_id):
        embed = discord.Embed(
            title=self.get_title(game_id),
            description=self.get_matrix(game_id),
            color=self.get_color(game_id)
        )
        embed.set_footer(text=utils.footer)
        view = View()
        for number in range(7):
            view.add_item(await self.make_button_number(game_id, number))

        if isinstance(context, commands.Context):
            await context.send(embed=embed, view=view)
        else:
            await context.response.edit_message(embed=embed, view=view)

    async def replay(self, context, game_id):
        embed = discord.Embed(
            title=self.get_title(game_id),
            description=self.get_matrix(game_id),
            color=self.get_color(game_id)
        )
        embed.set_footer(text=utils.footer)

        if isinstance(context, commands.Context):
            await context.send(embed=embed)
        else:
            await context.response.edit_message(embed=embed)

    async def make_button_number(self, game_id, number):
        async def callback(interaction):
            game_data = self.get_game_data(game_id)
            turn_player = self.bot.get_user(game_data.get("player_ids")[len(game_data.get("moves")) % 2])
            if interaction.user != turn_player:
                return

            if self.insert_chip(game_id, number) is not False:
                status = self.get_status(game_id)
                if status:
                    if status is True:
                        await self.send_draw_message(interaction.channel)
                    else:
                        await self.send_winner_message(interaction.channel, status)

                await self.game(interaction, game_id)

        button = Button(emoji=utils.numbers[number])
        button.callback = callback
        return button

    @staticmethod
    async def send_draw_message(channel):
        embed = discord.Embed(
            title="Draw",
            description="The game is drawn.",
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=utils.footer)
        await channel.send(embed=embed)

    @staticmethod
    async def send_winner_message(channel, winner):
        embed = discord.Embed(
            title="Win",
            description=f"{winner} has won the game, well played!",
            color=discord.Color.green()
        )
        embed.set_footer(text=utils.footer)
        await channel.send(embed=embed)

    @staticmethod
    async def error_game_not_found(context):
        embed = discord.Embed(
            title="Error: Game not found",
            description="The game you are looking for couldn't be found or does not exist.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)

    def get_title(self, game_id):
        game_data = self.get_game_data(game_id)
        players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
        turn_player = players[len(game_data.get("moves")) % 2]
        return f"Game: {game_id}; {' vs '.join(players)}\nIt's {turn_player}'s turn"

    def get_matrix(self, game_id):
        game_data = self.get_game_data(game_id)
        matrix = game_data.get("matrix")
        return "\n".join(["".join([utils.colors.get(cell_color) for cell_color in row]) for row in matrix])

    def get_color(self, game_id):
        game_data = self.get_game_data(game_id)
        return discord.Color.red() if len(game_data.get("moves")) % 2 == 0 else discord.Color.yellow()

    def insert_chip(self, game_id, column):
        game_data = self.get_game_data(game_id)
        matrix = game_data.get("matrix")
        moves = game_data.get("moves")
        color = "red" if len(moves) % 2 == 0 else "yellow"

        for row in reversed(matrix):
            if row[column] == "blue":
                row[column] = color
                moves.append(column)
                self.update_game_data(game_id, game_data)
                return True
        else:
            return False

    def get_status(self, game_id):
        game_data = self.get_game_data(game_id)
        players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
        turn_player = players[(len(game_data.get("moves")) % 2) - 1]

        if self.check_for_win(game_id):
            return turn_player
        return self.check_for_draw(game_id)

    def check_for_win(self, game_id):
        game_data = self.get_game_data(game_id)
        matrix = game_data.get("matrix")
        moves = game_data.get("moves")
        color = "red" if len(moves) % 2 == 1 else "yellow"
        root_x, root_y = moves[-1], 6 - game_data.get("moves").count(moves[-1])
        directions = {(1, 0): 1, (0, 1): 1, (1, 1): 1, (1, -1): 1}

        for i in range(2):
            factor = 1 - i*2
            for offsets, sequence in directions.items():
                offset_x, offset_y = [offset * factor for offset in offsets]
                new_x, new_y = root_x + offset_x, root_y + offset_y
                while self.is_in_bounds(new_x, new_y) and matrix[new_y][new_x] == color:
                    sequence += 1
                    if sequence == 4:
                        game_data["on_going"] = False
                        game_data["cur_move"] = len(moves)
                        self.update_game_data(game_id, game_data)
                        return True
                    new_x += offset_x
                    new_y += offset_y

    def check_for_draw(self, game_id):
        game_data = self.get_game_data(game_id)
        moves = game_data.get("moves")

        if len(moves) == 42:
            game_data["on_going"] = False
            game_data["cur_move"] = 42
            self.update_game_data(game_id, game_data)
            return True

    @staticmethod
    def is_in_bounds(x, y):
        return 0 <= x <= 6 and 0 <= y <= 5

    @staticmethod
    def get_game_data(game_id):
        with open("games.json") as outfile:
            json_file = json.load(outfile)
        return json_file.get(game_id)

    @staticmethod
    def update_game_data(game_id, game_data):
        with open("games.json") as outfile:
            json_file = json.load(outfile)
        print(json_file[game_id]["matrix"])
        with open("games.json", "w") as outfile:
            json_file[game_id] = game_data
            json.dump(json_file, outfile, indent=2)


async def generate_game_id(players):
    with open("games.json") as outfile:
        json_file = json.load(outfile)

    player_ids = [player.id for player in random.sample(players, k=2)]
    game_id = str(random.random())[-4:]
    while game_id in json_file:
        game_id = random.random()[-4:]

    json_file[game_id] = {
        "matrix": [["blue" for _ in range(7)] for _ in range(6)],
        "player_ids": player_ids,
        "moves": [],
        "on_going": True
    }

    with open("games.json", "w") as file:
        json.dump(json_file, file, indent=2)

    return game_id


async def setup(bot):
    await bot.add_cog(Game(bot))
