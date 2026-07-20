import sys

from admet_pipeline.core import catalog
from datetime import datetime
import json


def main(models, outputs):

    model_set = set(models)

    final_card = {}

    for i in catalog.endpoints:
        temp = {}
        output = None

        run = model_set.intersection(catalog.endpoints[i])
        if not run:
            continue
        for j in list(run):
            temp[j] = outputs[j]

        if catalog.endpoints_packages.get(i):         
            output = catalog.endpoints_packages[i].main(temp)
        
        final_card[i] = output

    with open("card"+datetime.now().isoformat()+".json", mode="w") as y:
        json.dump(final_card, y, indent=2)

    return

if __name__ == "__main__":
    sys.exit()