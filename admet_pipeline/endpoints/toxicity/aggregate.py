import sys
import json
from pathlib import Path

admet_ai_paths = [
            "DILI",                 
            "AMES",                 
            "ClinTox",              
            "Carcinogens_Lagunin",  
            "Skin_Reaction",        
            "hERG",                  
            "NR-AR",                
            "NR-AR-LBD",             
            "NR-AhR",                
            "NR-Aromatase",         
            "NR-ER",                
            "NR-ER-LBD",             
            "NR-PPAR-gamma",        
            "SR-ARE",               
            "SR-ATAD5", 
            "SR-HSE",              
            "SR-MMP",               
            "SR-p53",          
        ]

def _build_from_admet_ai(raw_admet_ai):
    final = {}

    for i in raw_admet_ai:
        final[i] = {key: raw_admet_ai[i][key] for key in admet_ai_paths if key in raw_admet_ai[i]}

    return final

def main(inp_paths):
    
    raw = {}

    for i in inp_paths:
        print(i)
        if i == "admet_ai":
            print('into the main frame')
            with open(Path(__file__).resolve().parent / i / inp_paths[i], mode="r") as y:
                all_admet_ai = json.load(y)
                raw[i] = _build_from_admet_ai(all_admet_ai)

    return raw

if __name__ == "__main__":
    sys.exit()

if __name__ == "__main__":
    sys.exit()