"""Calculates cmip6 ensemble mean"""

import cmip6.load as load
import cmip6.util as util

def main(scenario, variable, experiment, verbose=True):
    if verbose: print(f"Loading {load.arctic_ensemble_filepath(scenario, variable, experiment)}")
    returns


if __name__ == "__main__":
    scenario = "historical"
    variable = "siextentn"
    experiment = "r1i1p1f1"
    verbose=True
    
    main(scenario, variable, experiment, verbose=verbose)
    