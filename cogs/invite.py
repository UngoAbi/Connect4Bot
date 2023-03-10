import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot import utils
from Connect4Bot.connect4.c4game import start_new_game


class Invite(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"[LOAD] 'invite' command is loaded")

    @commands.command()
    async def invite(self, context: commands.Context, user: discord.Member) -> None:
        if user in [context.author, self.bot.user]:
            await self.send_error_invalid_user(context)
            return

        embed = discord.Embed(
            title="Invite has been sent",
            description=f"waiting for {user.mention} to respond",
            color=discord.Color.blue()
        )
        embed.set_footer(text=utils.footer)
        view = View()
        view.add_item(self.make_accept_button(context, user))
        view.add_item(self.make_reject_button(user))
        await context.send(embed=embed, view=view)

    def make_accept_button(self, context: commands.Context, user: discord.User) -> Button:
        async def callback(interaction: discord.Interaction) -> None:
            if interaction.user != user:
                return

            embed = discord.Embed(
                title="Invite has been accepted",
                description="Game has started",
                color=discord.Color.green()
            )
            embed.set_footer(text=utils.footer)
            await interaction.response.edit_message(embed=embed, view=None)

            game_id = start_new_game([context.author, user])
            await context.invoke(await self.bot.get_command("game")(context, game_id))

        button = Button(label="Accept", style=discord.ButtonStyle.green)
        button.callback = callback
        return button

    @staticmethod
    def make_reject_button(user: discord.User) -> Button:
        async def callback(interaction: discord.Interaction) -> None:
            if interaction.user != user:
                return

            embed = discord.Embed(
                title="Invite has been rejected",
                description="Game canceled",
                color=discord.Color.red()
            )
            embed.set_footer(text=utils.footer)
            await interaction.response.edit_message(embed=embed, view=None)

        button = Button(label="Reject", style=discord.ButtonStyle.red)
        button.callback = callback
        return button

    @staticmethod
    async def send_error_invalid_user(context: commands.Context) -> None:
        embed = discord.Embed(
            title="Error: Invalid user",
            description="You can't play with this user.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Invite(bot))
