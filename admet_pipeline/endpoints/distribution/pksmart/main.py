import pksmart
import os
from datetime import datetime
from admet_pipeline.endpoints import parser
import pandas as pd
import json

name = "pksmart"

def _run_pksmart(smiles):
    frames = []
    for i in smiles:
        frames.append(pksmart.predict_pk_params(i))

    return pd.concat(frames, ignore_index=True)

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

    predictions = _run_pksmart(smiles)

    formatted_predictions = predictions.set_index("smiles_r").to_dict(orient="index")

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(formatted_predictions, y, indent=2)

    print(f"result::{target}")


if __name__ == "__main__":
    main()