import json
from pathlib import Path
import sys
import admet_pipeline.endpoints.lipophilicity.logP.main as logP

admet_ai_logD= "Lipophilicity_AstraZeneca" 

def _build_from_admet_ai(raw_admet_ai, column_name):
    final = {}

    for i in raw_admet_ai:
        final[i] = raw_admet_ai[i][column_name]

    return final

def main(inp_paths):
    raw = {}

    for i in inp_paths:
        with open(inp_paths[i], mode = "r") as y:
            cur = json.load(y)
            if i == "molgpka":
                raw["crippen_logP_logD"] = logP.main(cur)
            elif i == "admet_ai":
                raw[i] = _build_from_admet_ai(cur, admet_ai_logD)
            else:
                raw[i] = cur

    return raw

if __name__ == "__main__":
    sys.exit()