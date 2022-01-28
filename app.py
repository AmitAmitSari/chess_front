import os
from flask import Flask, request, send_from_directory
# from flask_cors import CORS
import subprocess
from subprocess import PIPE

from engine_communications import read_board_from_engine, read_possible_moves_from_engine, send_move_to_engine

app = Flask(__name__, static_folder="./build")
# CORS(app)

state_map = {}


@app.route("/start_game")
def start_game():
    engine = subprocess.Popen(r"./chess_ai/target/release/xo_ai", stdin=PIPE, stdout=PIPE)
    board = read_board_from_engine(engine)
    possible_moves = read_possible_moves_from_engine(engine)

    key = max(state_map.keys(), default=0) + 1
    state_map[key] = {
        "engine": engine
    }
    return {
        "key": key,
        "board": board,
        "possible_moves": possible_moves
    }


class InvalidMove(Exception):
    pass


@app.route("/do_move", methods=["POST"])
def do_move():
    r = request.json
    state = state_map[r["key"]]
    engine = state['engine']

    ok, resp = send_move_to_engine(r["move"], engine)

    if not ok:
        raise InvalidMove(resp)

    board = read_board_from_engine(engine)
    board = read_board_from_engine(engine)
    possible_moves = read_possible_moves_from_engine(engine)

    print(board)
    print(possible_moves)

    return {
        "board": board,
        "possible_moves": possible_moves
    }


@app.route("/ping")
def ping():
    print("Ping")
    return "pong"


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("Serving", path)
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
