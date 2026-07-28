from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import sys
from admet_pipeline.endpoints.lipophilicity.logP import main as predict_logd

MPO_GATE = 4.0


def _ramp(x, good, bad):
    if x <= good:
        return 1.0
    if x >= bad:
        return 0.0
    return (bad - x) / (bad - good)


def _tpsa_score(tpsa):
    if tpsa <= 20.0:
        return 0.0
    if tpsa < 40.0:
        return (tpsa - 20.0) / 20.0
    return _ramp(tpsa, 90.0, 120.0)


def _most_basic_pka(sites):
    basic = [s["pka"] for s in sites if not s["pka_type"].startswith("acid")]
    return max(basic) if basic else 0.0


def cns_mpo(mol, logp, logd, sites):
    return (
        _ramp(Descriptors.MolWt(mol), 360.0, 500.0)
        + _ramp(logp, 3.0, 5.0)
        + _ramp(logd, 2.0, 4.0)
        + _ramp(_most_basic_pka(sites), 8.0, 10.0)
        + _tpsa_score(Descriptors.TPSA(mol))
        + _ramp(rdMolDescriptors.CalcNumHBD(mol), 0.5, 3.5)
    )


def main(data, ph=7.4):
    out = {}
    logd_out = predict_logd.main(data, ph)
    for smiles, sites in data.items():
        mol = Chem.MolFromSmiles(smiles)
        score = cns_mpo(mol, logd_out[smiles]["logP"], logd_out[smiles]["logD"], sites)
        out[smiles] = {"cns_mpo": round(score, 2), "cns_mpo_pass": score >= MPO_GATE}
    return out


if __name__ == "__main__":
    sys.exit()