import json
from pathlib import Path
import sys
import admet_pipeline.endpoints.distribution.cns_mpo.main as cns_mpo
import admet_pipeline.endpoints.distribution.bbb_score.main as bbb_score

admet_ai_bbb_vdss = ["VDss_Lombardo", "BBB_Martins"]

def _build_from_admet_ai(raw_admet_ai, column_names):
    final = {}

    for i in raw_admet_ai:
       final[i] = {key: raw_admet_ai[i][key] for key in column_names if key in raw_admet_ai[i]}

    return final

def main(inp_paths):
    raw = {}

    for i in inp_paths:
        with open(inp_paths[i], mode = "r") as y:
            cur = json.load(y)
            if i == "admet_ai":
                raw[i] = _build_from_admet_ai(cur, admet_ai_bbb_vdss)
            elif i == "molgpka":
                raw["cns_mpo"] = cns_mpo.main(cur)
                raw["bbb_score"] = bbb_score.main(cur) 
            elif i == "boiled_egg":
                ig = {}
                for j in cur:
                    ig[j] = {key: cur[j][key] for key in ["hia_s", "hia"]}
                raw[i] = ig
            else:
                raw[i] = cur
        

    return raw

if __name__ == "__main__":
    sys.exit()