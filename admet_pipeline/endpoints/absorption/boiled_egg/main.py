from pathlib import Path

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors
from admet_pipeline.endpoints import parser
import json
from datetime import datetime
from typing import List, Optional

name = "boiled_egg"

# Ellipse parameters recovered analytically from the boundary polygons in the
# supporting information of Daina & Zoete, ChemMedChem 2016, 11, 1117.
# Each entry is (cx, cy, Qxx, Qxy, Qyy) with Q normalised so the paper's
# boundary is exactly s = 1. Conic fit residual 3e-15; all 100 SI boundary
# points score 1.0000000000.
_ELLIPSE = {
    "hia": (71.0273620, 2.2945410, 2.1574256567e-04, 9.5755877420e-04, 5.2687498777e-02),
    "bbb": (38.0686490, 3.1849480, 5.9494943002e-04, 3.5699455958e-04, 1.2961161986e-01),
}


def _descriptors(mol):
    # includeSandP=True reproduces the published SwissADME calls; RDKit
    # defaults to False, which flips omeprazole to BBB+.
    return Descriptors.TPSA(mol, includeSandP=True), Crippen.MolLogP(mol)


def _score(tpsa, wlogp, key):
    cx, cy, qxx, qxy, qyy = _ELLIPSE[key]
    dx, dy = tpsa - cx, wlogp - cy
    return qxx * dx * dx + 2.0 * qxy * dx * dy + qyy * dy * dy


def boiled_egg(smiles):
    mol = Chem.MolFromSmiles(smiles)
    tpsa, wlogp = _descriptors(mol)
    hia = _score(tpsa, wlogp, "hia")
    bbb = _score(tpsa, wlogp, "bbb")
    return {
        "tpsa": tpsa,
        "wlogp": wlogp,
        "hia_s": hia,
        "hia": hia <= 1.0,
        "bbb_s": bbb,
        "bbb": bbb <= 1.0,
    }


def main(arg_inp: Optional[List[str]] = None):

    raw = {}

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    out_path = args.out

    data_path = args.input

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    for i in smiles:
        raw[i] = boiled_egg(i)

    output_path = datetime.now().isoformat().replace(":","_") + ".json"

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(raw, y, indent = 2)

    print(f"result::{target}")

    return

if __name__ == "__main__":
    main()