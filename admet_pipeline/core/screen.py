from argparse import Namespace
from pathlib import Path
import sys
import admet_pipeline.core.catalog as catalog
import admet_pipeline.core.runner as runner

def main(final_file: Path):

    runner.main(final_file)

    return

if __name__=="__main__":
    sys.exit()