import json
import sys

admet_ai_cyp = ["CYP1A2_Veith"
    "CYP2C19_Veith",
    "CYP2C9_Substrate_CarbonMangels",
    "CYP2C9_Veith",
    "CYP2D6_Substrate_CarbonMangels",
    "CYP2D6_Veith",
    "CYP3A4_Substrate_CarbonMangels",
    "CYP3A4_Veith"]

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
            raw[i] = _build_from_admet_ai(all, admet_ai_cyp)
        else:
            raw[i] = all

    return raw

if __name__ == "__main__":
    sys.exit()