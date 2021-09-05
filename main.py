import argparse
from game import Game
from constants import Role


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--r', type=str, default="OFFENSIVE", help='choose the role')
    parser.add_argument('-d', '--d', type=int, default=0, help='configure the machine intelligence')
    args = parser.parse_args()

    game = Game(Role[args.r], args.d)
    game.play()
