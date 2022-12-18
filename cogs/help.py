import os
import discord
from discord.ext import commands
from Connect4Bot.utils import create_embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'help' command is loaded")

    @commands.group(invoke_without_command=True)
    async def help(self, context):
        description = [f"`{filename[:-3]}`" for filename in os.listdir("./cogs") if (filename.endswith(".py"))]
        embed = create_embed(
            title="Commands",
            description=" ".join(description),
            color=discord.Color.blue()
        )
        await context.send(embed=embed)

    @help.command()
    async def invite(self, context):
        embed = create_embed(
            title="Invite",
            description="invites a user to a game",
            color=discord.Color.blue()
        )
        embed.add_field(name="Syntax:", value=f"**{self.bot.command_prefix}invite <user>**")
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
