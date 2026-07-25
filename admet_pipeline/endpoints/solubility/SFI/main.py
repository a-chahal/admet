import sys

from rdkit import Chem, RDLogger
from rdkit.Chem import rdMolDescriptors
import admet_pipeline.endpoints.solubility.aggregate as a
 
def _aromatic_ring_count(smiles):
    mol = Chem.MolFromSmiles(smiles)
    return rdMolDescriptors.CalcNumAromaticRings(mol)
 
 
def _sfi(smiles, logd):
    return float(logd) + _aromatic_ring_count(smiles)
 
 
def main(logd: dict):
    print(logd)
    return {s: _sfi(s, d) for s, d in logd.items()}

if __name__ == "__main__":
    sys.exit()