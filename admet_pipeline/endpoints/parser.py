import argparse
from pathlib import Path
import sys


def build_parser(name) -> argparse.ArgumentParser :
    parser = argparse.ArgumentParser(prog= "python -m admet_pipeline.endpoints." + name,
                                      description = "Screen molecules through" + name)
    
    parser.add_argument("--input", type=Path, help=".json of canonical SMILES + models to run", required=True)

    parser.add_argument("--out", type=Path, help="where to store output")

    return parser

if __name__=="__main__":
    sys.exit()