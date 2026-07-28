from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import sys

BBB_GATE = 4.0

_ARO_R = {0: 0.336367, 1: 0.816016, 2: 1.0, 3: 0.691115, 4: 0.199399}


def _poly(x, coeffs, norm, lo, hi):
    if not lo < x <= hi:
        return 0.0
    return sum(c * x ** i for i, c in enumerate(coeffs)) / norm


def _mwhbn(mol):
    hbn = rdMolDescriptors.CalcNumHBA(mol) + rdMolDescriptors.CalcNumHBD(mol)
    return hbn / Descriptors.MolWt(mol) ** 0.5


def _most_basic_pka(sites):
    basic = [s["pka"] for s in sites if not s["pka_type"].startswith("acid")]
    return max(basic) if basic else 0.0


def bbb_score(mol, sites):
    return (
        _ARO_R.get(rdMolDescriptors.CalcNumAromaticRings(mol), 0.0)
        + _poly(mol.GetNumHeavyAtoms(),
                (-0.463, 0.12775, -0.004556, 0.0000443), 0.624231, 5, 45)
        + 1.5 * _poly(_mwhbn(mol),
                      (-0.1358, 9.5202, -31.495, 26.733), 0.72258, 0.05, 0.45)
        + 2.0 * _poly(rdMolDescriptors.CalcTPSA(mol),
                      (0.9598, -0.0067), 0.9598, 0, 120)
        + 0.5 * _poly(_most_basic_pka(sites),
                      (0.8579, -0.71043, 0.18618, -0.016331, 0.00045068), 0.597488, 3, 11)
    )


def main(data, ph=7.4):
    out = {}
    for smiles, sites in data.items():
        mol = Chem.MolFromSmiles(smiles)
        score = bbb_score(mol, sites)
        out[smiles] = {"bbb_score": round(score, 2), "bbb_pass": score >= BBB_GATE}
    return out


if __name__ == "__main__":
    sys.exit()