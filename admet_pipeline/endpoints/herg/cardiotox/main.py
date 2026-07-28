import os, sys, types, json, contextlib
from pathlib import Path
from datetime import datetime

os.environ["CUDA_VISIBLE_DEVICES"] = ""

ROOT = Path(__file__).parent / "vendor" / "CardioTox"
sys.path[:0] = [str(ROOT), str(ROOT / "PyBioMed")]
sys.modules.setdefault("pybel", types.ModuleType("pybel"))  # PyBioMed imports it, never calls it

from rdkit import Chem
from rdkit.Chem import AllChem
import admet_pipeline.endpoints.parser as parser

name = "cardiotox"

# FVModel packs Morgan on-bit indices into a fixed 93-slot vector; more than that
# raises IndexError deep inside preprocessing.
MAX_ON_BITS = 93
BASE_MODEL_LABELS = {"fp": "fingerprint", "dm": "descriptor", "sv": "smiles_vector", "fv": "feature_vector"}


@contextlib.contextmanager
def _repo_cwd():
    previous = Path.cwd()
    os.chdir(ROOT)
    try:
        yield
    finally:
        os.chdir(previous)


def _on_bits(smile):
    mol = Chem.MolFromSmiles(smile)
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024).GetNumOnBits()


def _predict(smiles):
    with _repo_cwd():
        import cardiotox

        model = cardiotox.load_ensemble()

        # DescModel swallows scaler-load failures in a bare except and leaves normalizer=None,
        # which would otherwise surface as a confusing AttributeError mid-batch.
        if model.get_model("dm").normalizer is None:
            raise RuntimeError(
                "DescModel normalizer failed to unpickle - check the scikit-learn version "
                "against cardiotox/models/training_desc/normalizer.pickle"
            )

        # Preprocess once (mordred is the bottleneck) and reuse for ensemble + base models.
        features = model.preprocess_smile(smiles)
        ensemble = model.predict_preprocessed(features).ravel()
        base = {
            key: model.get_model(key).predict_preprocessed(x).ravel()
            for key, x in zip(model.model_order, features)
        }

    return {
        smile: {
            "hERG_blocker_probability": float(ensemble[i]),
            "hERG_blocker": bool(ensemble[i] > 0.5),
            **{
                "hERG_blocker_probability_" + label: float(base[key][i])
                for key, label in BASE_MODEL_LABELS.items()
            },
        }
        for i, smile in enumerate(smiles)
    }


def main(arg_inp=None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    out_path = args.out

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    in_domain = [smile for smile in smiles if _on_bits(smile) <= MAX_ON_BITS]

    predictions = _predict(in_domain) if in_domain else {}

    formatted_predictions = {
        smile: predictions.get(smile, {"error": "out_of_domain"}) for smile in smiles
    }

    output_path = datetime.now().isoformat().replace(":", "_") + ".json"

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(formatted_predictions, y, indent=2)

    print("result::" + str(target))


if __name__ == "__main__":
    main()