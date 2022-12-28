import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot import utils
from Connect4Bot.connect4 import c4game


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"[LOAD] 'game' command is loaded")

    @commands.command()
    async def game(self, context: commands.Context | discord.Interaction, game_id: str) -> None:
        game_data = c4game.get_game_data(game_id)
        if game_data is None:
            return

        match game_data.get("in_progress"):
            case True:
                await self.play(context, game_id)
            case False:
                await self.replay(context, game_data.copy())

    async def play(self, message: commands.Context | discord.Interaction, game_id: str) -> None:
        game_data = c4game.get_game_data(game_id)

        embed = discord.Embed(
            title=self.get_embed_title(game_data),
            description=self.get_game_ui(game_data.get("matrix")),
            color=c4game.get_turn_dccolor(game_data.get("current_turn"))
        )
        embed.set_footer(text=utils.footer)

        view = View()
        for number in range(7):
            view.add_item(self.make_number_button(game_id, number))

        if isinstance(message, commands.Context):
            await message.send(embed=embed, view=view)
        elif isinstance(message, discord.Interaction):
            await message.response.edit_message(embed=embed, view=view)

    async def replay(self, message: commands.Context | discord.Interaction, game_data: dict):
        embed = discord.Embed(
            title=self.get_embed_title(game_data),
            description=self.get_game_ui(game_data.get("matrix")),
            color=c4game.get_turn_dccolor(game_data.get("current_turn"))
        )
        embed.set_footer(text=utils.footer)

        view = View()

        if isinstance(message, commands.Context):
            view.add_item(self.make_left_arrow_button(game_data, message.author))
            view.add_item(self.make_right_arrow_button(game_data, message.author))
            await message.send(embed=embed, view=view)
        elif isinstance(message, discord.Interaction):
            view.add_item(self.make_left_arrow_button(game_data, message.user))
            view.add_item(self.make_right_arrow_button(game_data, message.user))
            await message.response.edit_message(embed=embed, view=view)

    def make_number_button(self, game_id: str, number: int) -> Button:
        async def callback(interaction: discord.Interaction) -> None:
            game_data = c4game.get_game_data(game_id)
            players = [self.bot.get_user(player_id) for player_id in game_data.get("player_ids")]
            turn_player = players[game_data.get("current_turn") % 2]

            if interaction.user != turn_player or c4game.insert_chip(game_data, number) is False:
                return

            moves = game_data.get("moves")
            moves.append(number)
            status = self.game_has_ended(game_data)
            if status:
                game_data["in_progress"] = False
                match status:
                    case str():
                        pass
                    case True:
                        pass

            c4game.set_game_data(game_id, game_data)
            await self.game(interaction, game_id)

        button = Button(emoji=utils.numbers[number])
        button.callback = callback
        return button

    def make_left_arrow_button(self, game_data: dict, user: discord.User) -> Button:
        async def callback(interaction: discord.Interaction) -> None:
            if interaction.user != user or game_data.get("current_turn") == 0:
                return

            current_turn = game_data.get("current_turn")
            previous_move = game_data.get("moves")[current_turn - 1]
            c4game.extract_chip(previous_move, game_data)
            await self.replay(interaction, game_data)

        button = Button(emoji=utils.arrows[0])
        button.callback = callback
        return button

    def make_right_arrow_button(self, game_data: dict, user: discord.User) -> Button:
        async def callback(interaction: discord.Interaction) -> None:
            if interaction.user != user or game_data.get("current_turn") == len(game_data.get("moves")):
                return

            current_turn = game_data.get("current_turn")
            next_move = game_data.get("moves")[current_turn]
            c4game.insert_chip(game_data, next_move)
            await self.replay(interaction, game_data)

        button = Button(emoji=utils.arrows[1])
        button.callback = callback
        return button

    def game_has_ended(self, game_data: dict) -> bool | str:
        if c4game.game_is_won(game_data):
            players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
            return players[(game_data.get("current_turn") % 2) - 1]
        return c4game.game_is_drawn(game_data)

    def get_embed_title(self, game_data: dict) -> str:
        players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
        turn_player = players[game_data.get("current_turn") % 2]
        return f"Game: {game_data.get('game_id')}; {' vs '.join(players)}\nIt's {turn_player}'s turn"

    @staticmethod
    def get_game_ui(matrix: list[list[str]]) -> str:
        return "\n".join(["".join([utils.colors.get(cell_color) for cell_color in row]) for row in matrix])

    @staticmethod
    async def send_error_game_not_found(context: commands.Context) -> None:
        embed = discord.Embed(
            title="Error: Game not found",
            description="The game you are looking for couldn't be found or does not exist.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)

    @staticmethod
    async def send_winner_message(channel: discord.TextChannel, winner: str) -> None:
        embed = discord.Embed(
            title="Win",
            description=f"{winner} has won the game, well played!",
            color=discord.Color.green()
        )
        embed.set_footer(text=utils.footer)
        await channel.send(embed=embed)

    @staticmethod
    async def send_draw_message(channel: discord.TextChannel) -> None:
        embed = discord.Embed(
            title="Draw",
            description="The game is drawn.",
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=utils.footer)
        await channel.send(embed=embed)


"""
@commands.command()
    async def game(self, context, game_id):
        game_data = self.get_game_data(game_id)

        match game_data.get("on_going"):
            case True:
                await self.play(context, game_id)
            case False:
                game_data = self.get_game_data(game_id)
                game_data["current_move"] = len(game_data.get("moves"))
                await self.replay(context, game_data)
            case None:
                await self.error_game_not_found(context)

    async def play(self, message, game_id):
        game_data = self.get_game_data(game_id)
        embed = discord.Embed(
            title=self.get_title(game_data),
            description=self.draw_matrix(game_data.get("matrix")),
            color=self.get_color(len(game_data.get("moves")))
        )
        embed.set_footer(text=utils.footer)

        view = View()
        for n in range(7):
            view.add_item(self.make_number_button(game_id, n))

        if isinstance(message, commands.Context):
            await message.send(embed=embed, view=view)
        else:
            await message.response.edit_message(embed=embed, view=view)

    async def replay(self, message, game_data):
        embed = discord.Embed(
            title=self.get_title(game_data),
            description=self.draw_matrix(game_data.get("matrix")),
            color=self.get_color(game_data.get("current_move"))
        )
        embed.set_footer(text=utils.footer)

        view = View()

        if isinstance(message, commands.Context):
            view.add_item(self.make_left_arrow_button(game_data, message.author))
            view.add_item(self.make_right_arrow_button(game_data, message.author))
            await message.send(embed=embed, view=view)
        else:
            view.add_item(self.make_left_arrow_button(game_data, message.user))
            view.add_item(self.make_right_arrow_button(game_data, message.user))
            await message.response.edit_message(embed=embed, view=view)

    def make_number_button(self, game_id, number):
        async def callback(interaction):
            game_data = self.get_game_data(game_id)
            turn_player = self.bot.get_user(game_data.get("player_ids")[len(game_data.get("moves")) % 2])
            if interaction.user != turn_player:
                return

            if self.insert_chip(game_data, number) is not False:
                game_data.get("moves").append(number)
                status = self.get_status(game_data)
                if status:
                    game_data["on_going"] = False
                    match status:
                        case str():
                            await self.send_winner_message(interaction.channel, status)
                        case True:
                            await self.send_draw_message(interaction.channel)

                self.update_game_data(game_id, game_data)
                await self.game(interaction, game_id)

        button = Button(emoji=utils.numbers[number])
        button.callback = callback
        return button

    def make_left_arrow_button(self, game_data, author):
        async def callback(interaction):
            if interaction.user != author or game_data.get("current_move") == 1:
                return

            game_data["current_move"] -= 1
            print(game_data.get("moves")[game_data.get("current_move")])
            self.extract_chip(game_data, game_data.get("moves")[game_data.get("current_move")])
            print(game_data)
            await self.replay(interaction, game_data)

        button = Button(emoji=utils.arrows[0])
        button.callback = callback
        return button

    def make_right_arrow_button(self, game_data, author):
        async def callback(interaction):
            if interaction.user != author or game_data.get("current_move") == len(game_data.get("move")):
                return

            self.insert_chip(game_data, game_data.get("moves")[game_data.get("current_move")])
            game_data["current_move"] += 1
            await self.replay(interaction, game_data)

        button = Button(emoji=utils.arrows[1])
        button.callback = callback
        return button

    @staticmethod
    def insert_chip(game_data, column):
        print(column)
        matrix = game_data.get("matrix")
        moves = game_data.get("moves")
        row = 5 - moves.count(column)
        if row == -1:
            return False
        color = "red" if len(moves) % 2 == 0 else "yellow"
        matrix[row][column] = color

    @staticmethod
    def extract_chip(game_data, column):
        print(column)
        matrix = game_data.get("matrix")
        moves = game_data.get("moves")
        row, column = 6 - moves.count(column), column
        matrix[row][column] = "blue"

    def get_status(self, game_data):
        if self.game_is_won(game_data):
            players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
            return players[(len(game_data.get("moves")) % 2) - 1]
        return self.game_is_draw(len(game_data.get("moves")))

    def get_title(self, game_data):
        players = [self.bot.get_user(player_id).name for player_id in game_data.get("player_ids")]
        turn_player = players[len(game_data.get("moves")) % 2]
        return f"Game: {game_data.get('game_id')}; {' vs '.join(players)}\nIt's {turn_player}'s turn"

    @staticmethod
    def draw_matrix(matrix):
        return "\n".join(["".join([utils.colors.get(cell_color) for cell_color in row]) for row in matrix])

    @staticmethod
    async def error_game_not_found(context):
        embed = discord.Embed(
            title="Error: Game not found",
            description="The game you are looking for couldn't be found or does not exist.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)

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
    async def send_draw_message(channel):
        embed = discord.Embed(
            title="Draw",
            description="The game is drawn.",
            color=discord.Color.light_gray()
        )
        embed.set_footer(text=utils.footer)
        await channel.send(embed=embed)"""


async def setup(bot):
    await bot.add_cog(Game(bot))
