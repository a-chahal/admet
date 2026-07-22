from vendor.RAscore.RAscore import RAscore_XGB
from admet_pipeline.endpoints import parser
import json
from datetime import datetime
from typing import List, Optional

name = "rascore"

def main(arg_inp: Optional[List[str]] = None):

    raw = {}

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    print(args)

    data_path = args.input

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    print(smiles)

    scorer = RAscore_XGB.RAScorerXGB()

    for i in smiles:
        raw[i] = float(scorer.predict(i))

    print(raw)

    output_path = datetime.now().isoformat().replace(":","_") + ".json"

    with open(output_path, mode="w") as y:
        json.dump(raw, y, indent = 2)

    print(f"result::{output_path}")

    return

if __name__ == "__main__":
    main()