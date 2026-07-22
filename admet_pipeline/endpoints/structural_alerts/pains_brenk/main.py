from rdkit import Chem
from admet_pipeline.endpoints import parser
import json
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from datetime import datetime

name = "pains_brenk"

def _flag(smiles, pains, brenk, nih):
    mol = Chem.MolFromSmiles(smiles)
    return {"pains": pains.HasMatch(mol), "brenk": brenk.HasMatch(mol), "nih": nih.HasMatch(mol)}

def _build(catalog_enum):
    p = FilterCatalogParams()
    p.AddCatalog(catalog_enum)
    return FilterCatalog(p)     

def main(arg_inp: list[str] | None = None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    with open(data_path, "r") as y:
        data = json.load(y)

    PAINS = _build(FilterCatalogParams.FilterCatalogs.PAINS)
    BRENK = _build(FilterCatalogParams.FilterCatalogs.BRENK)
    NIH = _build(FilterCatalogParams.FilterCatalogs.NIH)

    smiles = data["smiles"]

    output = {}

    for i in smiles:
        output[i] = _flag(i, PAINS, BRENK, NIH)

    output_path = datetime.now().isoformat().replace(":","_") + ".json"

    with open(output_path, mode="w") as y:
        json.dump(output, y, indent = 2)

    print(f"result::{output_path}")

    return

if __name__=="__main__":
    main()