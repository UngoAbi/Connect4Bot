import json
import random
import discord


def insert_chip(game_data: dict, column: int) -> bool:
    matrix = game_data.get("matrix")
    current_turn = game_data.get("current_turn")
    color = get_turn_color(current_turn)
    for row in reversed(matrix):
        if row[column] == "blue":
            row[column] = color
            game_data["current_turn"] += 1
            return True
    return False


def extract_chip(column: int, game_data: dict) -> None:
    matrix = game_data.get("matrix")

    for row in matrix:
        if row[column] != "blue":
            row[column] = "blue"
            game_data["current_turn"] -= 1
            return


def game_is_won(game_data: dict) -> bool:  # ToDo fix some bug here
    directions = ([(1, 0), 1], [(0, 1), 1], [(1, 1), 1], [(1, -1), 1])
    matrix = game_data.get("matrix")
    moves = game_data.get("moves")
    current_turn = game_data.get("current_turn")
    last_color = get_turn_color(current_turn - 1)
    last_move = moves[current_turn - 1], moves.count(moves[current_turn - 1])
    root_x, root_y = last_move

    for i in range(2):
        factor = 1 - 2*i
        for direction in directions:
            offset_x, offset_y = [offset * factor for offset in direction[0]]
            new_x, new_y = root_x + offset_x, root_y + offset_y

            while is_in_bounds(new_x, new_y) and matrix[new_y][new_x] == last_color:
                direction[1] += 1
                if direction[1] == 4:
                    return True

                new_x += offset_x
                new_y += offset_y
    return False


def game_is_drawn(game_data: dict) -> bool:
    moves = game_data.get("moves")
    return len(moves) == 42


def is_in_bounds(x: int, y: int) -> bool:
    return 0 <= x <= 6 and 0 <= y <= 5


def get_turn_color(turn_number: int) -> str:
    return "red" if turn_number % 2 == 0 else "yellow"


def get_turn_dccolor(turn_number: int) -> discord.Color:
    return discord.Color.red() if turn_number % 2 == 0 else discord.Color.yellow()


def start_new_game(players: list[discord.User]) -> str:
    game_id = make_game_id()
    player_ids = [player.id for player in random.sample(players, k=2)]
    game_data = {
        "game_id": game_id,
        "matrix": [["blue" for _ in range(7)] for _ in range(6)],
        "player_ids": player_ids,
        "moves": list(),
        "current_turn": 0,
        "in_progress": True
    }
    set_game_data(game_id, game_data)
    return game_id


def make_game_id() -> str:
    json_file = get_json_file()
    game_id = str(random.random())[-4:]
    while game_id in json_file:
        game_id = str(random.random())[-4:]
    return game_id


def set_game_data(game_id: str, game_data: dict) -> None:
    json_file = get_json_file()
    json_file[game_id] = game_data
    with open("./games.json", "w") as outfile:
        json.dump(json_file, outfile, indent=2)


def get_game_data(game_id: str) -> dict | None:
    json_file = get_json_file()
    return json_file.get(game_id)


def get_json_file() -> dict:
    with open("./games.json") as outfile:
        json_file = json.load(outfile)
    return json_file
