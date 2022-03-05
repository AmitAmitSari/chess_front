import os
from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
import subprocess
from subprocess import PIPE

from engine_communications import read_board_from_engine, read_possible_moves_from_engine, send_move_to_engine

app = Flask(__name__, static_folder="./build")

DEVELOP = False
options = {} if not DEVELOP else {"cors_allowed_origins": "*"}

socketio = SocketIO(app, **options)

state_map = {}


@socketio.on("connect")
def connect():
    print("Connecting")


@socketio.event
def start_game():
    print("start_game", request.sid)
    engine = subprocess.Popen(r"./chess_ai/target/release/xo_ai", stdin=PIPE, stdout=PIPE)
    state_map[request.sid] = engine

    board = read_board_from_engine(engine)
    print(board)
    emit("board", board)
    possible_moves = read_possible_moves_from_engine(engine)
    print(possible_moves)
    emit("possible_moves", possible_moves)

    return True


class InvalidMove(Exception):
    pass


@socketio.event
def do_move(json):
    print("do_move")
    engine = state_map[request.sid]
    r = json
    ok, resp = send_move_to_engine(r["move"], engine)

    if not ok:
        raise InvalidMove(resp)

    emit("board", read_board_from_engine(engine))
    emit("board", read_board_from_engine(engine))
    emit("possible_moves", read_possible_moves_from_engine(engine))

    return True


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
    socketio.run("0.0.0.0", 5000)
