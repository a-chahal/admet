from pathlib import Path
import sys
import os
import rdkit.Chem as Chem
from rdkit.Chem import RDConfig
import admet_pipeline.endpoints.parser as parser
from datetime import datetime

sys.path.append(os.path.join(RDConfig.RDContribDir, "SA_Score"))

import sys, os, admet_pipeline
import sascorer
import json
name = "sascore"

def main(arg_inp: list[str] | None = None):

    print('yurr')

    raw = {}

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    out_path = args.out

    data_path = args.input

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    for s in smiles:
        raw[s] = sascorer.calculateScore(Chem.MolFromSmiles(s))
        
    output_path = datetime.now().isoformat().replace(":","_") + ".json"

    target = out_path / name / output_path
    
    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(raw, y, indent = 2)

    print(f"result::{target}")

    return

if __name__ == "__main__":
    main()