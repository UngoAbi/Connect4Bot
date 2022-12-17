import json


with open("consts.json") as f:
    json_file = json.load(f)

    TOKEN = json_file["TOKEN"]
    OWNER_ID = json_file["OWNER_ID"]
    FOOTER = json_file["FOOTER"]
