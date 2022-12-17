import json


with open("constants.json") as f:
    json_file = json.load(f)
    TOKEN = json.load(f)["TOKEN"]

