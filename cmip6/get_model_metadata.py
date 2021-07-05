# Quick utility script to find metadata for models
#
# Metadata includes:
#     model name
#     path
#     ensembles
#     if areacello file exists
#     path to areacello
import os
import glob
from pprint import pprint

SICONC_PATH = "/home/apbarret/Data/CMIP6/siconc/SImon"
AREACELLO_PATH = "/home/apbarret/Data/CMIP6/areacello"


def ensemble_file_count(epath):
    """Returns number of files for a given ensembles"""
    return len(glob.glob(os.path.join(epath, '*')))

    
def find_ensembles(mpath, experiment='ssp370'):
    """Counts numbers of ensembles"""
    ensembles = glob.glob(os.path.join(mpath, experiment, '*'))
    return [os.path.basename(e) for e in ensembles if ensemble_file_count(e) > 0]


def find_areacello(model):
    """Returns areacello filename"""
    areacello_path = glob.glob(os.path.join(AREACELLO_PATH, f"*{model}*.nc"))
    if areacello_path:
        return os.path.basename(areacello_path[0])
    else:
        return []


def get_model_metadata(experiment='ssp370'):
    model_path = glob.glob(os.path.join(SICONC_PATH,'*'))
    metadata = {}
    for mp in model_path:
        model = os.path.basename(mp)
        metadata[model] = {
            'data_path': mp,
            'ensembles': find_ensembles(mp, experiment=experiment),
            'areacello': find_areacello(model),
        }
    return metadata


def list_ensembles(metadata, ensemble):
    d1 = {model: meta for model, meta in metadata.items() if ensemble in meta["ensembles"]}
    print(f"Models with {ensemble}")
    for i, m in enumerate(d1.keys(), 1):
          print(f"{i} {m}")
    print("")


def list_three_ensembles(metadata):
    d1 = {model: meta for model, meta in metadata.items() if len(meta["ensembles"]) == 3}
    print(f"Models with three ensembles")
    for i, m in enumerate(d1.keys(), 1):
          print(f"{i} {m}")
    print("")

    
def main():
    metadata = get_model_metadata()
    # Model with r1
    list_ensembles(metadata, "r1i1p1f1")
    # Models with r2
    list_ensembles(metadata, "r2i1p1f1")
    # Models with r3
    list_ensembles(metadata, "r3i1p1f1")

    # Models with 3 ensembles
    list_three_ensembles(metadata)


if __name__ == "__main__":
    main()
    
