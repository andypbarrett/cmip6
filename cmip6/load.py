"""Loader for CMIP6 data"""
from pathlib import Path

import pandas as pd


DATAPATH = Path("/home/apbarret/src/CMIP6/data")


def arctic_ensemble_filepath(scenario, variable, experiment):
    """Returns filepath for file matching scenario, experiment and variable"""
    return DATAPATH / f"cmip6_{variable}_{scenario}_{experiment}.from_siconc.csv"

    
def cmip6_ensemble(scenario, experiment, variable="siextentn"):
    """Loads csv file of sea ice variable ensemble into pandas dataframe

    :scenario: historical, ssp370, ssp585
    :experiment: experiment id, e.g. r1i1p1f1
    :variable: siarean, siextentn

    :returns: pandas dataframe
    """
    df = pd.read_csv(arctic_ensemble_filepath(scenario, variable, experiment),
                     index_col = "time",
                     parse_dates = True)
    return df
