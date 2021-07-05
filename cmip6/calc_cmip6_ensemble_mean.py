"""Calculates cmip6 ensemble statistics"""
from pathlib import Path
import re

import cmip6.load as load
import cmip6.util as util


def parse_filepath(fp):
    return re.split('\.|_', fp.name)[1:4]


def get_ensemble_stats_filepath(fp):
    """Returns new filepath for ensemble stats"""
    new_name = fp.name.replace(".from_siconc", "_ensemble_stats.from_siconc")
    return fp.with_name(new_name)

    
def calc_smip6_ensemble_stats(ensemble_filepath, verbose=True):
    ensemble_filepath = Path(ensemble_filepath)
    ensemble_stats_filepath = get_ensemble_stats_filepath(ensemble_filepath)

    variable, scenario, experiment = parse_filepath(ensemble_filepath)

    if verbose: print(f"Getting ensemble statistics for {ensemble_filepath}")
    
    if verbose: print(f"   loading file...")
    ensemble_df = load.cmip6_ensemble(scenario, experiment, variable)

    if verbose: print("   calculating ensemble statistics...")
    ensemble_stats_df = util.get_ensemble_stats(ensemble_df)

    if verbose: print(f"   writing ensemble statistics to {ensemble_stats_filepath}")
    ensemble_stats_df.to_csv(ensemble_stats_filepath)
    
    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculates ensemble statistics")
    parser.add_argument("ensemble_filepath", type=str, help="Path for file to process")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    
    calc_smip6_ensemble_stats(args.ensemble_filepath, verbose=args.verbose)
    
