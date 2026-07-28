from enum import Enum
import sys
import admet_pipeline.endpoints.generalist.aggregate
import admet_pipeline.endpoints.structural_alerts.aggregate
import admet_pipeline.endpoints.synthesizability.aggregate
import admet_pipeline.endpoints.toxicity.aggregate
import admet_pipeline.endpoints.lipophilicity.aggregate
import admet_pipeline.endpoints.solubility.aggregate
import admet_pipeline.endpoints.metabolism.aggregate
import admet_pipeline.endpoints.permeability.aggregate
import admet_pipeline.endpoints.absorption.aggregate
import admet_pipeline.endpoints.distribution.aggregate
import  admet_pipeline.endpoints.herg.aggregate


class Models():
    admet_ai = "admet_ai"
    pains_brenk = "pains_brenk"
    rascore = "rascore" 
    sascore = "sascore"
    # qupkake = "qupkake"
    molgpka = "molgpka"
    smartcyp = "smartcyp"
    boiled_egg = "boiled_egg"
    pksmart = "pksmart"
    bayesherg = "bayesherg"
    cardiotox = "cardiotox"


endpoints = {
    "generalist" : set({Models.admet_ai}),
    "herg" : set({Models.admet_ai, Models.bayesherg, Models.cardiotox}),
    "metabolism" : (set({Models.admet_ai, Models.smartcyp})),
    "clearance" : set(),
    "distribution" : set({Models.admet_ai, Models.pksmart, Models.boiled_egg, Models.molgpka}),
    "solubility" : set({Models.admet_ai}),
    "lipophilicity" : set({Models.molgpka, Models.admet_ai}),
    "absorption": set({Models.admet_ai, Models.boiled_egg}),
    "permeability" : set({Models.admet_ai}),
    "structural_alerts" : set({Models.pains_brenk}),
    "synthesizability" : set({Models.rascore, Models.sascore}),
    "toxicity" : set({Models.admet_ai}),
}

paths = {
    Models.admet_ai: "admet_pipeline/endpoints/generalist/admet_ai",
    Models.pains_brenk: "admet_pipeline/endpoints/structural_alerts/pains_brenk",
    Models.rascore: "admet_pipeline/endpoints/synthesizability/rascore",
    Models.sascore: "admet_pipeline/endpoints/synthesizability/sascore",
    Models.molgpka : "admet_pipeline/endpoints/lipophilicity/molgpka",
    Models.smartcyp: "admet_pipeline/endpoints/metabolism/smartcyp",
    Models.boiled_egg: "admet_pipeline/endpoints/absorption/boiled_egg",
    Models.pksmart: "admet_pipeline/endpoints/distribution/pksmart",
    Models.bayesherg: "admet_pipeline/endpoints/herg/bayesherg",
    Models.cardiotox: "admet_pipeline/endpoints/herg/cardiotox"
}

endpoints_packages = {
    # "generalist": admet_pipeline.endpoints.generalist.aggregate,
    "structural_alerts": admet_pipeline.endpoints.structural_alerts.aggregate,
    "synthesizability": admet_pipeline.endpoints.synthesizability.aggregate,
    "toxicity": admet_pipeline.endpoints.toxicity.aggregate,
    "lipophilicity": admet_pipeline.endpoints.lipophilicity.aggregate,
    "solubility": admet_pipeline.endpoints.solubility.aggregate,
    "metabolism": admet_pipeline.endpoints.metabolism.aggregate,
    "permeability": admet_pipeline.endpoints.permeability.aggregate,
    "absorption": admet_pipeline.endpoints.absorption.aggregate,
    "distribution": admet_pipeline.endpoints.distribution.aggregate,
    "herg": admet_pipeline.endpoints.herg.aggregate,
}

if __name__ == "__main__":
    sys.exit()