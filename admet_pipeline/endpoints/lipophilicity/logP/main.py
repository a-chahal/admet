import math 
from rdkit import Chem
from rdkit.Chem import Crippen
import sys
 
 
def _log10_1p10(x):
    return max(x, 0.0) + math.log10(1 + 10 ** -abs(x))
 
 
def log_d(logp, sites, ph=7.4):
    return logp - sum(
        _log10_1p10(ph - s["pka"] if s["pka_type"].startswith("acid") else s["pka"] - ph)
        for s in sites
    )
 
 
def main(data, ph=7.4):
    out = {}
    for smiles, sites in data.items():
        mol = Chem.MolFromSmiles(smiles)
        logp = Crippen.MolLogP(mol)
        out[smiles] = {"logP": logp, "logD": log_d(logp, sites, ph)}
    return out
 
 
if __name__ == "__main__":
    sys.exit()