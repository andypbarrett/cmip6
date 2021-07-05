import xarray as xr

DATAPATH = "/home/apbarret/Data/CMIP6/from_julienne"


def read_names_file(names_file):
    with (DATAPATH / names_file).open("r") as f:
        names = f.read()
    return names


def parse_names(names):
    """Splits names into (model, experiment) tuples and returns as list"""
    pass


