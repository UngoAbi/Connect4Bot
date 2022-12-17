import discord
from discord.ext import commands
from discord.ui import Button, View
from Connect4Bot.utils import create_embed


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'Invite' command is loaded")

    @commands.command()
    async def invite(self, context, user: discord.Member):
        if user == context.message.author or user == self.bot.user:
            embed = create_embed(
                title="Error",
                description="You cannot invite with this user",
                color=discord.Color.red()
            )
            await context.send(embed=embed)
            return

        embed = create_embed(
            title="Invite sent",
            description=f"Waiting for {user.mention} to respond",
            color=discord.Color.blue()
        )

        accept_button = create_accept_button(user)
        reject_button = create_reject_button(user)
        view = View()
        view.add_item(accept_button)
        view.add_item(reject_button)

        await context.send(embed=embed, view=view)


def create_accept_button(user):
    button = Button(label="Accept", style=discord.ButtonStyle.green)

    async def callback(interaction):
        if interaction.user == user:
            embed = create_embed(
                title="Invite has been accepted",
                color=discord.Color.green()
            )
            await interaction.response.edit_message(embed=embed, view=None)

    button.callback = callback

    return button


def create_reject_button(user):
    button = Button(label="Reject", style=discord.ButtonStyle.red)

    async def callback(interaction):
        if interaction.user == user:
            embed = create_embed(
                title="Invite has been rejected",
                color=discord.Color.red()
            )
            await interaction.response.edit_message(embed=embed, view=None)

    button.callback = callback

    return button


async def setup(bot):
    await bot.add_cog(Invite(bot))
