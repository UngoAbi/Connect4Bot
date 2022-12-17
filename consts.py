import json


with open("consts.json") as f:
    json_file = json.load(f)

    token = json_file["TOKEN"]
    owner_id = json_file["OWNER_ID"]
    footer = json_file["FOOTER"]
