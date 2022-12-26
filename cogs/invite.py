import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot import utils
from Connect4Bot.cogs.game import generate_game_id


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'invite' command is loaded")

    @commands.command()
    async def invite(self, context, user: discord.Member):
        if user in (context.message.author, self.bot.user):
            self.send_error_invalid_user(context)

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

    def make_accept_button(self, context, user):
        async def callback(interaction):
            if interaction.user != user:
                return

            embed = discord.Embed(
                title="Invite has been accepted",
                description="Game has started",
                color=discord.Color.green()
            )
            embed.set_footer(text=utils.footer)
            await interaction.response.edit_message(embed=embed, view=None)

            game_id = generate_game_id([context.author, user])
            await context.invoke(await self.bot.get_command("game")(context, game_id))

        button = Button(label="Accept", style=discord.ButtonStyle.green)
        button.callback = callback
        return button

    @staticmethod
    def make_reject_button(user):
        async def callback(interaction):
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
    async def send_error_invalid_user(context):
        embed = discord.Embed(
            title="Error: Invalid user",
            description="You can't play with this user.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Invite(bot))
