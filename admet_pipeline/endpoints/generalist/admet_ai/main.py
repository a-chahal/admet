import sys
import os
import admet_pipeline.endpoints.parser as parser
import json

from admet_ai import ADMETModel # type: ignore

name = "admet_ai"

def main(arg_inp: list[str] | None = None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input
    
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    model = ADMETModel()

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]
    
    predictions = []
    
    for i in smiles:

        preds = model.predict(i)

        predictions.append(preds)
    
    print(predictions)

    return predictions

if __name__ == "__main__":
    sys.exit()