import sys
import admet_pipeline.core.catalog as catalog
import admet_pipeline.core.runner as runner

def main():
    
    runnables = set()

    endpoints = catalog.endpoints

    for i in endpoints.keys():
        runnables.update(endpoints[i])

    runner.main(list(runnables))

    return

if __name__=="__main__":
    sys.exit(main())