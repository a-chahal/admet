from enum import Enum
import sys

class Models():
    admet_ai = "admet_ai"

endpoints = {
    "generalist" : set({Models.admet_ai}),
    "herg" : set({Models.admet_ai}),
    "metabolism" : ({Models.admet_ai}),
    "clearance" : set(),
    "distribution" : set(),
    "ppb" : set(),
    "solubility" : set({Models.admet_ai}),
    "lipophilicity" : set(),
    "permeability" : set(),
    "structural_alerts" : set(),
    "synthesizability" : set(),
    "toxicity" : set(),
    "druglikeness" : set(),
}

paths = {
    Models.admet_ai: "admet_pipeline/endpoints/generalist/admet_ai"
}

if __name__ == "__main__":
    sys.exit()