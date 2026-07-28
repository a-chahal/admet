import json
import sys

admet_ai_distr = ["HIA_Hou", "Bioavailability_Ma"]

def _build_from_admet_ai(raw_admet_ai, column_names):
    final = {}

    for i in raw_admet_ai:
         final[i] = {key: raw_admet_ai[i][key] for key in column_names if key in raw_admet_ai[i]}


    return final

def main(inp_paths):
    
    raw = {}

    for i in inp_paths:
        with open(inp_paths[i]) as y:
            all = json.load(y)
        if i == "admet_ai":
            raw[i] = _build_from_admet_ai(all, admet_ai_distr)
        elif i == "boiled_egg":
            ig = {}
            for j in all:
                ig[j] = {key: all[j][key] for key in ["hia_s", "hia"]}
            raw[i] = ig
        else:
            raw[i] = all

    return raw

if __name__ == "__main__":
    sys.exit()