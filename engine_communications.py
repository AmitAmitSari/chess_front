from typing import List
import subprocess


def readline(engine: subprocess.Popen) -> str:
    return engine.stdout.readline().replace(b'\n', b'').decode("utf-8")


def read_board_from_engine(engine: subprocess.Popen) -> List[List[str]]:
    board = [[""] * 8 for i in range(8)]
    piece_count = int(readline(engine))
    for i in range(piece_count):
        x, y, piece_type = readline(engine).split()
        board[int(x)][int(y)] = piece_type
    return board


def read_possible_moves_from_engine(engine: subprocess.Popen) -> List[str]:
    moves = []
    moves_count = int(readline(engine))
    for i in range(moves_count):
        moves.append(readline(engine))
    return moves


def send_move_to_engine(move: str, engine: subprocess.Popen) -> (bool, str):
    mv = (move + "\n").encode("utf-8")
    print("sending move:", mv)

    engine.stdin.write(mv)
    engine.stdin.flush()
    print("reading resp")
    resp = readline(engine)
    print("returning with resp", resp)
    return resp == "GOOD", resp
