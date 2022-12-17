import discord
from consts import footer


def create_embed(title=None, description=None, color=None):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer)
    return embed
