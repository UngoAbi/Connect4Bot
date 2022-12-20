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
    async def invite(self, context, user:discord.Member):
        if not isinstance(user, discord.Member):
            self.error_user_not_found(context)
            return

        if user == context.message.author or user == self.bot.user:
            self.error_invalid_user(context)
            return

        embed = discord.Embed(
            title="Invited sent",
            description=f"waiting for {user.mention} to respond.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=utils.footer)
        view = View()
        view.add_item(await self.make_button_accept(context, user))
        view.add_item(await self.make_button_reject(user))
        await context.send(embed=embed, view=view)

    async def make_button_accept(self, context, user):
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
            game_id = await generate_game_id([context.author, user])
            await context.invoke(await self.bot.get_command("game")(context, game_id))

        button = Button(label="Accept", style=discord.ButtonStyle.green)
        button.callback = callback
        return button

    @staticmethod
    async def make_button_reject(user):
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
    async def error_user_not_found(context):
        embed = discord.Embed(
            title="Error: User not found",
            description="The user you are looking for couldn't be found or does not exist.\nYou need to mention/ping the user, you want to play with.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)

    @staticmethod
    async def error_invalid_user(context):
        embed = discord.Embed(
            title="Error: Invalid user",
            description="You can't play with this user.",
            color=discord.Color.dark_red()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Invite(bot))
