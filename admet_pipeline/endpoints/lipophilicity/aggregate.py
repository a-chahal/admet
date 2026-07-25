import json
from pathlib import Path
import sys
import admet_pipeline.endpoints.lipophilicity.logP.main as logP

def main(inp_paths):
    raw = {}

    for i in inp_paths:
        with open(inp_paths[i], mode = "r") as y:
            if i == "qupkake":
                        raw["crippen_logP_logD"] = logP.main(json.load(y))
            raw[i] = json.load(y)

    return raw

if __name__ == "__main__":
    sys.exit()