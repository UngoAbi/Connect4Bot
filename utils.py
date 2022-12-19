import json
import discord


def create_embed(title=None, description=None, color=None):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer)
    return embed


with open("consts.json") as file:
    json_file = json.load(file)

token = json_file["TOKEN"]
owner_id = json_file["OWNER_ID"]
footer = json_file["FOOTER"]

blue_square = "🟦"
red_circle = "🔴"
yellow_circle = "🟡"
numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
