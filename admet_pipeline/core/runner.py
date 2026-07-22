import os
import subprocess
import sys
from admet_pipeline.core import aggregate
import admet_pipeline.core.catalog as catalog
import json
from pathlib import Path

def main(file_path: Path):

    outputs = {}

    with open(file_path, mode="r") as y:
        inp = json.load(y)

    models = inp["models"]

    abs_input = str(Path(file_path).resolve())

    repo_root = Path(__file__).resolve().parents[2]

    for i in models:
        print(i)
        endpoint = repo_root / catalog.paths[i]
        env = {**os.environ, "PYTHONPATH": str(repo_root)}

        result = subprocess.run(
            ["pixi", "run", "python", "main.py", "--input", abs_input],
            cwd=endpoint,
            env=env,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        print(result.stderr)

        paths = [l.split("::", 1)[1] for l in result.stdout.splitlines() if l.startswith("result::")]
        print(paths)
        final_path = paths[-1]
        
        outputs[i] = final_path
    aggregate.main(models, outputs)

    return

if __name__ == "__main__":
    sys.exit()