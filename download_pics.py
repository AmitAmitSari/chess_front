import requests


def main():
    for color in "wb":
        for name in "bknpqr":
            resp = requests.get(f"https://images.chesscomfiles.com/chess-themes/pieces/neo/150/{color}{name}.png")
            with open(f"./my_frontend/frontend/build/static/media/{color}{name}.png", "wb") as f:
                f.write(resp.content)


if __name__ == "__main__":
    main()
