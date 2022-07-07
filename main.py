from config import DEVELOPER_MODE
from game import Game


if __name__ == "__main__":
    if DEVELOPER_MODE:
        print("DEVELOPER_MODE enabled")
    game = Game()
    game.play()
