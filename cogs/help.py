import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("help command is loaded")

    @commands.command()
    async def help(self, context):
        await context.send("insert text")


async def setup(bot):
    await bot.add_cog(Help(bot))
