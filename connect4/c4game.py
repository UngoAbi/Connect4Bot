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


def is_in_bounds(x, y):
    return 0 <= x <= 6 and 0 <= y <= 5
