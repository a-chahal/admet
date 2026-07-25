from enum import Enum
import sys
import admet_pipeline.endpoints.generalist.aggregate
import admet_pipeline.endpoints.structural_alerts.aggregate
import admet_pipeline.endpoints.synthesizability.aggregate
import admet_pipeline.endpoints.toxicity.aggregate
import admet_pipeline.endpoints.lipophilicity.aggregate
import admet_pipeline.endpoints.solubility.aggregate

class Models():
    admet_ai = "admet_ai"
    pains_brenk = "pains_brenk"
    rascore = "rascore" 
    sascore = "sascore"
    qupkake = "qupkake"

endpoints = {
    "generalist" : set({Models.admet_ai}),
    "herg" : set(),
    "metabolism" : (),
    "clearance" : set(),
    "distribution" : set(),
    "ppb" : set(),
    "solubility" : set({Models.admet_ai}),
    "lipophilicity" : set({Models.qupkake}),
    "permeability" : set(),
    "structural_alerts" : set({Models.pains_brenk}),
    "synthesizability" : set({Models.rascore, Models.sascore}),
    "toxicity" : set({Models.admet_ai}),
    "druglikeness" : set(),
}

paths = {
    Models.admet_ai: "admet_pipeline/endpoints/generalist/admet_ai",
    Models.pains_brenk: "admet_pipeline/endpoints/structural_alerts/pains_brenk",
    Models.rascore: "admet_pipeline/endpoints/synthesizability/rascore",
    Models.sascore: "admet_pipeline/endpoints/synthesizability/sascore",
    Models.qupkake : "admet_pipeline/endpoints/lipophilicity/qupkake",
}

endpoints_packages = {
    # "generalist": admet_pipeline.endpoints.generalist.aggregate,
    "structural_alerts": admet_pipeline.endpoints.structural_alerts.aggregate,
    "synthesizability": admet_pipeline.endpoints.synthesizability.aggregate,
    "toxicity": admet_pipeline.endpoints.toxicity.aggregate,
    "lipophilicity": admet_pipeline.endpoints.lipophilicity.aggregate,
    "solubility": admet_pipeline.endpoints.solubility.aggregate
}

if __name__ == "__main__":
    sys.exit()