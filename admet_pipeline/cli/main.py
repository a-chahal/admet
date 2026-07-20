import argparse
from pathlib import Path
import sys
from admet_pipeline.core import screen
import pandas as pd
from rdkit import Chem
import admet_pipeline.core.catalog as catalog
import csv
from datetime import datetime
import json

def _build_parser() -> argparse.ArgumentParser :
    parser = argparse.ArgumentParser(prog="python -m admet_pipeline.cli",
                                      description = "Screen molecules through ADMET pipeline")
    
    parser.add_argument("--input", type=Path, help="a .smi file or csv of SMILES", required=True)
    
    models = parser.add_mutually_exclusive_group(required=False)
    models.add_argument("-w", help="Models to run")
    models.add_argument("-wo", help="Models to run without")

    parser.add_argument("--out", type=Path, help="where to store output")

    return parser

def _clean_input(input_path: Path):
    input_file = pd.read_csv(input_path)

    final_inp = set()

    for i in input_file.itertuples():
        mol = Chem.MolFromSmiles(i.SMILES)

        if mol:
            final_inp.add(Chem.CanonSmiles(i.SMILES))

    return final_inp

def _build_model_list(w: str | None  = None, wo: str | None  = None):

    runnables = set()

    for i in catalog.endpoints.keys():
        runnables.update(catalog.endpoints[i])

    if not w and not wo:
        return runnables

    if wo:
        return runnables - set(wo.split(" "))

    if w:
       return runnables.intersection(set(w.split(" ")))
    
    

def _build_final_file(input_path: Path, w: str | None  = None, wo: str | None  = None):

    final_inp = _clean_input(input_path)
    runnables = _build_model_list(w, wo)

    if runnables is None:
        runnables = []

    final_file = {
        "smiles": list(final_inp),
        "models": list(runnables),
    }

    file_name = "admet_pipeline/endpoints/final_file" + datetime.now().isoformat() + ".json"

    with open(file_name, mode="w") as y:
        json.dump(final_file, y, indent = 2)

    return Path(file_name)

def main(arg_inp: list[str] | None = None):
    args = _build_parser().parse_args(arg_inp)

    final_file = _build_final_file(args.input, args.w, args.wo)

    screen.main(final_file)

    return

if __name__=="__main__":
    sys.exit()