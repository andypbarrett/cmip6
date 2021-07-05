# Searches ESGF using API and compares with data I have downloaded and processed
import requests
import os
import glob

import pandas as pd


SEARCH_URL = "http://esgf-node.llnl.gov/esg-search/search/?offset=0&limit=50&type=Dataset&replica=false&latest=true&mip_era=CMIP6&experiment_id=ssp370&variant_label={}&table_id=SImon&variable_id=siconc&project=CMIP6&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"
RESULTS_PATH = "."


def search_esgf(variant_id):
    """Searches ESGF CMIP6 archive and returns json object containing results"""
    response = requests.get(SEARCH_URL.format(variant_id))
    return response.json()


def get_esgf_models(variant_id):
    """Returns list of models matching ESGF search"""
    response = search_esgf(variant_id)
    return [entry["source_id"][0] for entry in response["response"]["docs"]]


def get_processed_models(ensemble):
    """Returns list of processed models from csv results file header"""
    results_file = os.path.join(RESULTS_PATH, f'cmip6_siarean_ssp370_{ensemble}.from_siconc.csv')
    df = pd.read_csv(results_file, header=0, index_col=0)
    return list(df.columns)


def search_and_compare_esgf(variant_id, experiment='ssp370'):

    esgf_set = set(get_esgf_models(variant_id))
    print(f"Models found on ESGF: {len(esgf_set)}")
    
    processed_set = set(get_processed_models(variant_id))
    print(f"Models processed: {len(processed_set)}")

    print("Models on ESGF not processed locally:")
    for model in sorted(esgf_set.difference(processed_set)):
        print(model)


if __name__ == "__main__":
    variant_id = 'r3i1p1f1'
    search_and_compare_esgf(variant_id)
    
