from enum import Enum
import sys
import admet_pipeline.endpoints.generalist.aggregate
import admet_pipeline.endpoints.structural_alerts.aggregate

class Models():
    admet_ai = "admet_ai"
    pains_brenk = "pains_brenk"

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
    "structural_alerts" : set({Models.pains_brenk}),
    "synthesizability" : set(),
    "toxicity" : set(),
    "druglikeness" : set(),
}

paths = {
    Models.admet_ai: "admet_pipeline/endpoints/generalist/admet_ai",
    Models.pains_brenk: "admet_pipeline/endpoints/structural_alerts/pains_brenk"
}

endpoints_packages = {
    "generalist": admet_pipeline.endpoints.generalist.aggregate,
    "structural_alerts": admet_pipeline.endpoints.structural_alerts.aggregate
}

if __name__ == "__main__":
    sys.exit()