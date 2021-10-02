import argparse
from game import Game


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    game = Game()
    game.play()
