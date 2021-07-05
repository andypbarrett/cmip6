"""Calculates cmip6 ensemble mean"""

import cmip6.load as load
import cmip6.util as util


def get_ensemble_stats_filepath(fp):
    """Returns new filepath for ensemble stats"""
    new_name = fp.name.replace(".from_siconc", "_ensemble_stats.from_siconc")
    return fp.with_name(new_name)

    
def main(scenario, variable, experiment, verbose=True):
    ensemble_filepath = load.arctic_ensemble_filepath(scenario, variable, experiment)
    ensemble_stats_filepath = get_ensemble_stats_filepath(ensemble_filepath)
    
    if verbose: print(f"Loading {ensemble_filepath}")
    ensemble_df = load.cmip6_ensemble(scenario, experiment, variable)
    
    ensemble_stats_df = util.get_ensemble_stats(ensemble_df)

    ensemble_stats_df.to_csv(ensemble_stats_filepath)
    
    return


if __name__ == "__main__":
    scenario = "historical"
    variable = "siextentn"
    experiment = "r1i1p1f1"
    verbose=True
    
    main(scenario, variable, experiment, verbose=verbose)
    
