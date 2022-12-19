from utils import blue_square, red_circle, yellow_circle


def insert_chip(data, column):
    state = data.get("state")
    moves = data.get("moves")
    chip = "1" if (len(moves) % 2 == 0) else "2"

    for row in reversed(state):
        if row[column] == "0":
            row[column] = chip
            moves.append(column)
            return data
    else:
        return False


def get_title(bot, data, game_id):
    player1, player2 = players = [bot.get_user(player_id) for player_id in data.get("players")]
    turn_player = players[len(data.get("moves")) % 2]
    return f"Game: {game_id} {player1} vs {player2}\nIt's {turn_player}'s turn"


def get_grid(data):
    state = data.get("state")
    grid = ""

    for row in state:
        for cell in row:
            if cell == "0":
                grid += blue_square
            elif cell == "1":
                grid += red_circle
            else:
                grid += yellow_circle
        grid += "\n"
    return grid


def is_in_bounds(x, y):
    return 0 <= x <= 6 and 0 <= y <= 5
