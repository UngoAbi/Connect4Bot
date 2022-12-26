import json


with open("consts.json") as file:
    json_file = json.load(file)

token = json_file["token"]
owner_id = json_file["owner_id"]

footer = "Connect4 BOT made with discord.py by UngoAbi#7629"

colors = {"blue": "🟦", "red": "🔴", "yellow": "🟡"}
numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
arrows = ["⬅️", "➡️"]
