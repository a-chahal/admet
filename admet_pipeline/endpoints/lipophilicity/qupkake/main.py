from pathlib import Path
import os
import tempfile
import admet_pipeline.endpoints.parser as parser
import json
from datetime import datetime

import pandas as pd
from rdkit.Chem import PandasTools
from qupkake.cli import process_file
from qupkake.predict import run_prediction_pipeline
import logging
logging.basicConfig(level=logging.ERROR, format="%(message)s")

name = "qupkake"

COLUMNS = ["smiles", "idx", "pka_type", "pka"]


def run_qupkake(smiles: list[str]) -> pd.DataFrame:

    with tempfile.TemporaryDirectory() as root:

        for d in ("raw", "processed", "logs", "output"):
            os.makedirs(f"{root}/{d}", exist_ok=True)

        names = [str(i) for i in range(len(smiles))]

        pd.DataFrame({"smiles": smiles, "name": names}).to_csv(
            f"{root}/input.csv", index=False
        )

        staged = process_file(
            f"{root}/input.csv", smiles_col="smiles", name_col="name", root=root
        )

        run_prediction_pipeline(
            root=root,
            filename=staged,
            tautomerize=False,
            name_col="name",
            mol_col="ROMol",
            mp=False,
            output="out.sdf",
        )

        out = Path(root) / "output" / "out.sdf"

        if not out.exists():
            return pd.DataFrame(columns=COLUMNS)

        df = PandasTools.LoadSDF(
            str(out), idName="name", embedProps=True, removeHs=False
        )

    df["smiles"] = df["name"].astype(int).map(dict(enumerate(smiles)))
    df["idx"] = df["idx"].astype(int)
    df["pka"] = df["pka"].astype(float)

    return df[COLUMNS].reset_index(drop=True)


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

    predictions = run_qupkake(smiles)

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