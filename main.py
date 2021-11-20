import time
import subprocess
from subprocess import PIPE, STDOUT

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


CHROMEDRIVER = r"C:\Users\amits\Downloads\chromedriver.exe"


class Game:

    def __init__(self):
        self.positions = set()

    def init(self, board):
        self.positions = set(self.get_positions(board))

    def find_move_and_update(self, board, should_move):
        """

        :param board:
        :param should_move: should either be 'b' or 'w'
        :return:
        """
        new_positions = set(self.get_positions(board))

        if any(len(pos) != 2 for pos in new_positions):
            return None

        added = set(filter(lambda pos: pos[0][0] == should_move, new_positions.difference(self.positions)))
        removed = set(filter(lambda pos: pos[0][0] == should_move, self.positions.difference(new_positions)))

        if len(added) == 0 or len(removed) == 0:
            return None

        if len(new_positions) != len(set(pos[1] for pos in new_positions)):
            # If there is more than one piece in the same square.
            return None

        self.positions = new_positions

        if len(added) > 1:
            added = set(filter(lambda pos: pos[0][1] in "kK", added))
        assert len(added) == 1

        to_square = added.pop()
        from_square = None
        for r in removed:
            if r[0] == to_square[0] or r[0][1] in "pP":
                from_square = r

        assert from_square is not None
        new_type = ""
        if from_square[0] != to_square[0]:
            print(removed)
            print(added)
            print(from_square)
            print(to_square)
            new_type = to_square[0][1]

        return self.letter_pos(from_square) + self.letter_pos(to_square) + new_type

    @staticmethod
    def do_move(driver, board, move):
        if len(move) == 4:
            fr = f"{'abcdefgh'.index(move[0]) + 1}{move[1]}"
            to = f"{'abcdefgh'.index(move[2]) + 1}{move[3]}"
            from_square = list(filter(lambda elem: f"square-{fr}" in elem.get_attribute("class"),
                                      board.find_elements(By.CLASS_NAME, "piece")))
            assert len(from_square) == 1

            from_square[0].click()
            time.sleep(0.1)

            to_square = list(filter(lambda elem: f"square-{to}" in elem.get_attribute("class"),
                                    board.find_elements(By.CLASS_NAME, "hint") + board.find_elements(By.CLASS_NAME, "capture-hint")))
            assert len(to_square) == 1

            ac = ActionChains(driver)
            ac.move_to_element(to_square[0]).click().perform()

        else:
            print(move)
            print("Promote pawn for me plz")
            # Pawn promotion

    @staticmethod
    def get_positions(board):
        pieces = board.find_elements(By.CLASS_NAME, "piece")
        for piece in pieces:
            # Should look like: ("bp", "square-17")
            pos = tuple(
                sorted(filter(lambda x: x != "piece", piece.get_attribute("class").split()), key=lambda x: len(x)))
            yield pos

    @staticmethod
    def letter_pos(pos):
        """
        17 to a7 ect
        """
        nums = pos[1].split("-")[1]
        letter = nums[0].translate(nums.maketrans("12345678", "abcdefgh"))
        return f"{letter}{nums[1]}"


def main():

    driver = webdriver.Chrome(CHROMEDRIVER)
    engine = subprocess.Popen(r"C:\Users\amits\work\rust\projects\xo_ai\target\release\xo_ai.exe", stdin=PIPE, stdout=PIPE)

    # White
    engine_player = 0

    try:
        driver.get("https://www.chess.com/play/computer")
        board = driver.find_element(By.TAG_NAME, "chess-board")

        input("Press enter to start.")

        cur_player = 0

        g = Game()
        g.init(board)

        while True:
            if cur_player == engine_player:
                engine_move = engine.stdout.readline().replace(b'\n', b'').decode("utf-8")
                g.do_move(driver, board, engine_move)
                a = g.find_move_and_update(board, "wb"[engine_player])
                while not a:
                    a = g.find_move_and_update(board, "wb"[engine_player])
            else:
                a = g.find_move_and_update(board, "bw"[engine_player])
                while not a:
                    a = g.find_move_and_update(board, "bw"[engine_player])
                print(f"Sending {a} to engine")
                engine.stdin.write((a + "\r\n").encode("utf-8"))
                engine.stdin.flush()

                res = engine.stdout.readline().replace(b'\n', b'').decode("utf-8")
                while res != "GOOD":
                    print("Move was not ok, enter correct move. res:", res)
                    move = input("Enter Move, ")
                    engine.stdin.write((move + "\r\n").encode("utf-8"))
                    engine.stdin.flush()
                    res = engine.stdout.readline().replace(b'\n', b'').decode("utf-8")

            cur_player = 1 - cur_player

        elem = driver.find_element(By.CLASS_NAME, "bk")

        print(elem.id, elem.tag_name, elem.text)
        time.sleep(2)
        elem.click()

        input()
    except Exception:
        driver.close()
        raise


if __name__ == '__main__':
    main()
