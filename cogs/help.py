import os
import discord
from discord.ext import commands
from Connect4Bot import utils


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'help' command is loaded")

    @commands.group(invoke_without_command=True)
    async def help(self, context):
        description = [f"`{filename[:-3]}`" for filename in os.listdir("./cogs") if (filename.endswith(".py"))]
        embed = discord.Embed(
            title="Commands",
            description=" ".join(description),
            color=discord.Color.blue()
        )
        embed.set_footer(text=utils.footer)
        await context.send(embed=embed)

    @help.command()
    async def invite(self, context):
        embed = discord.Embed(
            title="Invite",
            description="invites a user to a game",
            color=discord.Color.blue()
        )
        embed.set_footer(text=utils.footer)
        embed.add_field(name="Syntax:", value=f"**{self.bot.command_prefix}invite <user>**")
        await context.send(embed=embed)

    @help.command()
    async def game(self, context):
        embed = discord.Embed(
            title="Game",
            description="display an on going game or watch a replay",
            color=discord.Color.blue()
        )
        embed.set_footer(text=utils.footer)
        embed.add_field(name="Syntax:", value=f"**{self.bot.command_prefix}game <game_id>**")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
