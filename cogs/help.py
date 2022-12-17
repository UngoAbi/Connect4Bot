import discord
from discord.ext import commands
from Connect4Bot.consts import FOOTER


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOAD] 'help' command is loaded")

    @commands.group(invoke_without_command=True)
    async def help(self, context):
        embed = discord.Embed(
            title="help",
            description="shows a list of all commands",
            color=discord.Color.blue()
        )
        embed.set_footer(text=FOOTER)
        await context.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
