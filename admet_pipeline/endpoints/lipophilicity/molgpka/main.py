from pathlib import Path
import os
import sys
import types
import json
from datetime import datetime

import pandas as pd
from rdkit import Chem
import admet_pipeline.endpoints.parser as parser

import logging
logging.basicConfig(level=logging.ERROR, format="%(message)s")

MOLGPKA_SRC = Path(__file__).resolve().parent / "vendor" / "MolGpKa" / "src"
sys.path.insert(0, str(MOLGPKA_SRC))

if "torch_scatter" not in sys.modules:
    import torch

    def _scatter_add(src, index, dim=-1, out=None, dim_size=None):
        if dim < 0:
            dim = src.dim() + dim
        if dim_size is None:
            dim_size = int(index.max()) + 1 if index.numel() else 0
        shape = list(src.shape)
        shape[dim] = dim_size
        idx = index
        while idx.dim() < src.dim():
            idx = idx.unsqueeze(-1)
        idx = idx.expand_as(src)
        base = out if out is not None else src.new_zeros(shape)
        return base.scatter_add_(dim, idx, src)

    _ts = types.ModuleType("torch_scatter")
    _ts.scatter_add = _scatter_add
    sys.modules["torch_scatter"] = _ts


import utils.ionization_group as _ig
_ig.smarts_file = str(MOLGPKA_SRC / "utils" / "smarts_pattern.tsv")

from predict_pka import predict

name = "molgpka"

COLUMNS = ["smiles", "idx", "pka_type", "pka"]


def _run_molgpka(smiles: list[str]) -> pd.DataFrame:

    rows = []

    for smi in smiles:

        mol = Chem.MolFromSmiles(smi)

        if mol is None:
            continue

        base_dict, acid_dict = predict(mol)

        for aid, pka in base_dict.items():
            rows.append({"smiles": smi, "idx": int(aid), "pka_type": "basic", "pka": float(pka)})

        for aid, pka in acid_dict.items():
            rows.append({"smiles": smi, "idx": int(aid), "pka_type": "acidic", "pka": float(pka)})

    if not rows:
        return pd.DataFrame(columns=COLUMNS)

    return pd.DataFrame(rows)[COLUMNS].reset_index(drop=True)


def main(arg_inp: list[str] | None = None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    out_path = args.out

    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    output_path = datetime.now().isoformat().replace(":", "_") + ".json"

    predictions = _run_molgpka(smiles)

    formatted_predictions = {s: [] for s in smiles}

    for smi, g in predictions.groupby("smiles", sort=False):
        formatted_predictions[smi] = g.drop(columns="smiles").to_dict(orient="records")

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(formatted_predictions, y, indent=2)

    print(f"result::{target}")


if __name__ == "__main__":
    main()