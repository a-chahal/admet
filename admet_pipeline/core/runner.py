import subprocess
import sys
import admet_pipeline.core.catalog as catalog

def main(runnables):
    for i in runnables:
        result = subprocess.run(["pixi", "run", 
                        "--manifest-path", "pixi.toml", 
                        "python", "main.py"], cwd=catalog.paths[i], 
                    capture_output=True, 
                    text=True)
        
        print(result.stderr, end="")
        print(result.stdout, end = "", file=sys.stderr)
    
    return

if __name__ == "__main__":
    sys.exit()