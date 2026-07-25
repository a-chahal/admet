from pathlib import Path
import sys
import os
import admet_pipeline.endpoints.parser as parser
import json
from datetime import datetime

from admet_ai import ADMETModel # type: ignore

name = "admet_ai"

def main(arg_inp: list[str] | None = None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    out_path = args.out

    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    model = ADMETModel()

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    output_path = datetime.now().isoformat().replace(":","_") + ".json"
    
    predictions = model.predict(smiles)

    formatted_predictions = predictions.to_dict(orient="index")

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(formatted_predictions, y, indent=2)
    
    print(f"result::{target}")

if __name__ == "__main__":
    main()