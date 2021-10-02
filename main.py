import argparse
import os
from game import Game


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default=os.environ.get("DEV_MODE"), help='set developer mode')
    args = parser.parse_args()

    game = Game(developer_mode=bool(args.d))
    game.play()
