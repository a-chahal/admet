from pathlib import Path
import sys
import admet_pipeline.endpoints.parser as parser
import json
from datetime import datetime

import pandas as pd

REPO = Path(__file__).resolve().parents[0] / "vendor" / "BayeshERG"
sys.path.insert(0, str(REPO))

from dgl.data.chem import CanonicalAtomFeaturizer, CanonicalBondFeaturizer  # type: ignore
from main import load_data, load_model, prediction  # type: ignore

name = "bayesherg"

SAMPLES = 30


def main(arg_inp=None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    out_path = args.out

    model = load_model(str(REPO / "model" / "model_weights.pth"), "cpu")

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    output_path = datetime.now().isoformat().replace(":", "_") + ".json"

    df = pd.DataFrame({"smiles": smiles})
    graphs = load_data(df, CanonicalAtomFeaturizer(), CanonicalBondFeaturizer())
    predictions, _, _ = prediction(model, df, graphs, "cpu", samples=SAMPLES)

    formatted_predictions = predictions.set_index("smiles").to_dict(orient="index")

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(formatted_predictions, y, indent=2)

    print(f"result::{target}")


if __name__ == "__main__":
    main()