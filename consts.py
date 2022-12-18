import json


with open("consts.json") as file:
    json_file = json.load(file)

token = json_file["TOKEN"]
owner_id = json_file["OWNER_ID"]
footer = json_file["FOOTER"]
