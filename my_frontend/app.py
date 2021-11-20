
from flask import Flask, render_template
import subprocess
from subprocess import PIPE

app = Flask(__name__)


ENGINE = None


def readline(engine: subprocess.Popen):
    return engine.stdout.readline().replace(b'\n', b'').decode("utf-8")


def read_board_from_engine(engine: subprocess.Popen):
    board = [[None] * 8 for i in range(8)]
    piece_count = int(readline(engine))
    for i in range(piece_count):
        x, y, piece_type = readline(engine).split()
        board[int(x)][int(y)] = piece_type
    return board


def read_possible_moves_from_engine(engine: subprocess.Popen):
    moves = []
    moves_count = int(readline(engine))
    for i in range(moves_count):
        moves.append(readline(engine))
    return moves


@app.route("/")
def main_screen():
    global ENGINE
    if ENGINE is not None:
        ENGINE.terminate()

    ENGINE = subprocess.Popen(r"C:\Users\amits\work\rust\projects\xo_ai\target\release\xo_ai.exe", stdin=PIPE, stdout=PIPE)
    board = read_board_from_engine(ENGINE)
    possible_moves = read_possible_moves_from_engine(ENGINE)
    print(len(possible_moves))
    print(possible_moves)

    return render_template("start_screen.html", board=board, possible_moves=possible_moves)


if __name__ == "__main__":
    app.run()
