import json
from pathlib import Path
import sys

def main(inp_paths):
    raw = {}

    for i in inp_paths:
        with open(Path(__file__).resolve().parent / i / inp_paths[i], mode="r") as y:
            raw[i] = json.load(y)

    return raw

if __name__ == "__main__":
    sys.exit()