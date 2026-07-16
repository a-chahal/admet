import sys

from admet_ai import ADMETModel # type: ignore

def main():
    model = ADMETModel()
    preds = model.predict(smiles="O(c1ccc(cc1)CCOC)CC(O)CNC(C)C")

    return preds

if __name__ == "__main__":
    sys.exit(main())