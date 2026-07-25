import admet_pipeline.endpoints.solubility.SFI.main as sfi
import json
import sys

admet_ai_logD = "Lipophilicity_AstraZeneca"
admet_ai_logS = "Solubility_AqSolDB" #log(mol/L)

def _build_from_admet_ai(raw_admet_ai, column_name):
    final = {}

    for i in raw_admet_ai:
        final[i] = raw_admet_ai[i][column_name]

    return final

def main(inp_paths):
    
    raw = {}

    for i in inp_paths:
        print(i)
        if i == "admet_ai":
            print('into the main frame')
            with open(inp_paths[i]) as y:
                all_admet_ai = json.load(y)
                admet_ai_logD_preds = _build_from_admet_ai(all_admet_ai, admet_ai_logD)
                raw["SFI"] = sfi.main(admet_ai_logD_preds)
            raw[i] = _build_from_admet_ai(all_admet_ai, admet_ai_logS)

    return raw

if __name__ == "__main__":
    sys.exit()

if __name__ == "__main__":
    sys.exit()