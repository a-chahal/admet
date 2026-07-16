import argparse
from pathlib import Path
import sys
from admet_pipeline.core import screen

def _build_parser() -> argparse.ArgumentParser :
    parser = argparse.ArgumentParser(prog="python -m admet_pipeline.cli",
                                      description = "Screen molecules through ADMET pipeline")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--smiles", help="a single molecule SMILES to screen")
    src.add_argument("--input", type=Path, help="a .smi file or csv of SMILES")
    
    models = parser.add_mutually_exclusive_group(required=False)
    models.add_argument("-w", help="Models to run")
    models.add_argument("-wo", help="Models to run without")

    parser.add_argument("--out", type=Path, help="where to store output")

    return parser

def main(arg_inp: list[str] | None = None):
    args = _build_parser().parse_args(arg_inp)

    print(args.w)

    screen.main()

    return

if __name__=="__main__":
    sys.exit()