import json
from datetime import datetime
from pathlib import Path

from rdkit import Chem, RDLogger
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams

from admet_pipeline.endpoints import parser

RDLogger.DisableLog("rdApp.*")

name = "pains_brenk"

_BUILTIN = {
    "pains_a": FilterCatalogParams.FilterCatalogs.PAINS_A,
    "pains_b": FilterCatalogParams.FilterCatalogs.PAINS_B,
    "pains_c": FilterCatalogParams.FilterCatalogs.PAINS_C,
    "brenk":   FilterCatalogParams.FilterCatalogs.BRENK,
    "nih":     FilterCatalogParams.FilterCatalogs.NIH,
}


def _build_builtin(catalog_enum) -> FilterCatalog:
    p = FilterCatalogParams()
    p.AddCatalog(catalog_enum)
    return FilterCatalog(p)


def _load_custom(alerts_dir: Path) -> dict:
    sets = {}
    for f in sorted(alerts_dir.glob("*.json")):
        spec = json.loads(f.read_text())
        compiled = []
        for a in spec["alerts"]:
            patt = Chem.MolFromSmarts(a["smarts"])
            if patt is None:
                raise ValueError(f"bad SMARTS in {f.name}: {a['name']} -> {a['smarts']}")
            compiled.append((a["name"], a["smarts"], patt))
        sets[spec["set"]] = {"reference": spec.get("reference", ""), "alerts": compiled}
    return sets


def _match_builtin(mol, set_name, catalog) -> list[dict]:
    hits = []
    for fm in catalog.GetFilterMatches(mol):
        idx = sorted({m for _, m in fm.atomPairs})
        hits.append({
            "set": set_name,
            "alert": fm.filterMatch.GetName() or "unnamed",
            "atoms": idx,
        })
    # GetMatches() carries the curated description; merge it in
    for entry, hit in zip(catalog.GetMatches(mol), hits):
        hit["description"] = entry.GetDescription()
    return hits


def _match_custom(mol, set_name, spec) -> list[dict]:
    hits = []
    for alert_name, smarts, patt in spec["alerts"]:
        for match in mol.GetSubstructMatches(patt, uniquify=True):
            hits.append({
                "set": set_name,
                "alert": alert_name,
                "smarts": smarts,
                "atoms": sorted(match),
            })
    return hits


def _profile(smiles, builtins, customs) -> dict:
    mol = Chem.MolFromSmiles(smiles)

    hits = []
    for set_name, catalog in builtins.items():
        hits.extend(_match_builtin(mol, set_name, catalog))
    for set_name, spec in customs.items():
        hits.extend(_match_custom(mol, set_name, spec))

    regions = {frozenset(h["atoms"]) for h in hits if h["atoms"]}
    return {
        "hits": hits,
        "sets_fired": sorted({h["set"] for h in hits}),
        "n_alerts": len(hits),
        "n_regions": len(regions),   # dedup: one furan counted once
    }


def main(arg_inp: list[str] | None = None):
    p = parser.build_parser(name)
    args = p.parse_args(arg_inp)

    data = json.loads(Path(args.input).read_text())
    alerts_dir = Path(getattr(args, "alerts_dir", None) or
                      Path(__file__).parent / "data" / "alerts")

    builtins = {k: _build_builtin(v) for k, v in _BUILTIN.items()}
    customs = _load_custom(alerts_dir)

    output = {s: _profile(s, builtins, customs) for s in data["smiles"]}

    out_path = Path(args.out)
    target = out_path / name / (datetime.now().isoformat().replace(":", "_") + ".json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2))

    print(f"result::{target}")

if __name__ == "__main__":
    main()