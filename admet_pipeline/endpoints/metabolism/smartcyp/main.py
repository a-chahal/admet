from pathlib import Path
import csv
import json
import os
import subprocess
import tempfile
from datetime import datetime

import admet_pipeline.endpoints.parser as parser

name = "smartcyp"

JAR = Path(__file__).resolve().parent / "vendor" / "smartcyp-2.4.2.jar"

# Columns SMARTCyp emits per atom. "Molecule" is a 1-based index into the
# input file, not a name -- the mapping back to SMILES is positional.
INT_FIELDS = {"Ranking", "2D6ranking", "2Cranking", "Span2End", "N+Dist", "COODist"}
FLOAT_FIELDS = {"Score", "Energy", "Relative Span", "2D6score", "2Cscore", "2DSASA"}


def _coerce(field: str, raw: str):
    raw = raw.strip()
    if raw == "":
        return None
    try:
        if field in INT_FIELDS:
            return int(float(raw))
        if field in FLOAT_FIELDS:
            return float(raw)
    except ValueError:
        return raw
    return raw


def run_smartcyp(smiles: list[str], jar: Path = JAR) -> dict[str, list[dict]]:

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        infile = tmp / "input.smi"
        infile.write_text("\n".join(smiles) + "\n")

        proc = subprocess.run(
            [
                "java",
                "-Djava.awt.headless=true",
                "-jar",
                str(jar),
                str(infile),
                "-outputdir",
                str(tmp),
                "-outputfile",
                "smartcyp",
                "-nohtml",
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"SMARTCyp exited {proc.returncode}\n"
                f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
            )

        csv_path = tmp / "smartcyp.csv"
        if not csv_path.is_file():
            raise RuntimeError(f"SMARTCyp produced no CSV\nstdout:\n{proc.stdout}")

        by_index: dict[int, list[dict]] = {}
        with csv_path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                idx = int(row.pop("Molecule"))
                by_index.setdefault(idx, []).append(
                    {field: _coerce(field, value) for field, value in row.items()}
                )

    # SMARTCyp silently drops molecules its CDK 1.4.8 parser rejects, which
    # would shift every subsequent index. Fail loudly instead of misaligning.
    missing = sorted(set(range(1, len(smiles) + 1)) - by_index.keys())
    if missing:
        raise RuntimeError(
            f"SMARTCyp returned results for {len(by_index)} of {len(smiles)} "
            f"molecules; missing input indices (1-based): {missing}"
        )

    return {smiles[idx - 1]: atoms for idx, atoms in sorted(by_index.items())}


def main(arg_inp: list[str] | None = None):

    p = parser.build_parser(name)

    args = p.parse_args(arg_inp)

    data_path = args.input

    out_path = args.out

    with open(data_path, "r") as y:
        data = json.load(y)

    smiles = data["smiles"]

    output_path = datetime.now().isoformat().replace(":", "_") + ".json"

    predictions = run_smartcyp(smiles)

    target = out_path / name / output_path

    target.parent.mkdir(parents=True, exist_ok=True)

    with open(target, mode="w") as y:
        json.dump(predictions, y, indent=2)

    print(f"result::{target}")


if __name__ == "__main__":
    main()