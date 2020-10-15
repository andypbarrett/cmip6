import os
import glob

import pandas as pd
import datetime as dt

import siconc

experiment = "historical"
ensemble = "r1i1p1f1"

EXCLUDE_THESE_MODELS = ['CESM2-WACCM']

def process_one_model(model, experiment, ensemble):
    """Calculate siarean and siextentn for one model"""
    
    try:
        siconc_ds, area_ds = siconc.load_data(model, experiment, ensemble)
    except Exception as error:
        raise Exception(error)

    siarean = siconc.calc_siarean(siconc_ds, area_ds)
    siextentn = siconc.calc_siextentn(siconc_ds, area_ds)

    siconc_ds.close()
    area_ds.close()

    return siarean, siextentn


def siconc_to_northern_hemisphere(experiment, ensemble, verbose=False):
    """Batch routine to calculate northern hemisphere sea ice extent and area"""

    if verbose:
        print(f"Processing CMIP6 files for:")
        print(f"   experiment: {experiment}")
        print(f"   ensembles: {ensemble}")
        
    siarean_dct = {}
    siextentn_dct = {}
    for model in siconc.model_list():
        
        if model in EXCLUDE_THESE_MODELS:
            continue
        
        print(f"Processing {model}...")
        try:
            siarean, siextentn = process_one_model(model, experiment, ensemble)
        except Exception as error:
            print(error)
            print("Skipping...\n")
            continue
        
        siarean_dct[model] = siarean.to_series()
        siextentn_dct[model] = siextentn.to_series()
    
    siarean_df = pd.DataFrame(siarean_dct)
    siextentn_df = pd.DataFrame(siextentn_dct)

    siextentn_out_file = f"cmip6_siextentn_{experiment}_{ensemble}.from_siconc.csv"
    if verbose: print(f"Writing siextentn to {siextentn_out_file}")
    siextentn_df.to_csv(siextentn_out_file)

    siarean_out_file = f"cmip6_siarean_{experiment}_{ensemble}.from_siconc.csv"
    if verbose: print(f"Writing siarean to {siarean_out_file}")
    siarean_df.to_csv(siarean_out_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch processor for CMIP6 siconc to Northern Hemisphere extent and area")
    parser.add_argument("experiment", type=str, help="standard CMIP6 experiment name")
    parser.add_argument("ensemble", type=str, help="CMIP6 ensemble identifier")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    
    siconc_to_northern_hemisphere(args.experiment, args.ensemble, verbose=args.verbose)
