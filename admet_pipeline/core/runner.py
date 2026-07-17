import os
import subprocess
import sys
import admet_pipeline.core.catalog as catalog
import json
from pathlib import Path

def main(file_path: Path):

    with open(file_path, mode="r") as y:
        inp = json.load(y)

    models = inp["models"]

    print(models)

    abs_input = str(Path(file_path).resolve())

    repo_root = Path(__file__).resolve().parents[2]

    for i in models:
        endpoint = repo_root / catalog.paths[i]
        env = {**os.environ, "PYTHONPATH": str(repo_root)}

        result = subprocess.run(
            ["pixi", "run", "python", "main.py", "--input", abs_input],
            cwd=endpoint,
            env=env,
            capture_output=True,
            text=True,
        )
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
    
    return

if __name__ == "__main__":
    sys.exit()