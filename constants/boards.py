import os


BOARDS = {}
DIR = "boards"
for file in os.listdir(DIR):
    path = DIR + '/' + file
    with open(path, "r") as f:
        lines = f.readlines()
    lines = [line.replace('\n', '').replace('.', ' ') for line in lines]
    if len(lines) != 10 or any(len(line) != 9 for line in lines):
        raise ValueError(f"{path}: wrong board format. ")
    BOARDS[file.split('.')[0]] = tuple(lines)
