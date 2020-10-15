"""Functions to process CMIP6 siconc grids"""
import os
import glob
import datetime as dt
import cftime

import xarray as xr

# TODO: move to constants.py
DATA_PATH = "/home/apbarret/Data/CMIP6"
SICONC_PATH = os.path.join(DATA_PATH, "siconc", "SImon")
AREACELLO_PATH = os.path.join(DATA_PATH, "areacello")

MAXTIME = cftime.DatetimeNoLeap(2100, 12, 31)

def model_list():
    """Returns a list of models to process"""
    return [os.path.basename(p) for p in glob.glob(os.path.join(SICONC_PATH, '*'))]


def find_siconc_files(model, experiment, ensemble):
    files = glob.glob(os.path.join(SICONC_PATH, model, experiment, ensemble, "*.nc"))
    if not files:
        raise Exception(f"No siconc files found for {model} {experiment} {ensemble}")
    return files


def get_siconc(filepaths):
    '''Returns xarray.Dataset for a given model run'''
    ds = xr.open_mfdataset(filepaths, combine="by_coords", use_cftime=True, data_vars=['siconc'])
    if ds.time.dt.year.max() > 2100:
        print(f"time exceeds datetime limit: truncating time axis to 2100-12-31")
        ds = ds.sel(time=slice(None, '2100-12-31'))
    if 'lat' in ds.variables:
        ds = ds.rename({'lat': 'latitude', 'lon': 'longitude'})
    if 'ni' in ds.dims:
        ds = ds.rename_dims({'ni': 'i', 'nj': 'j'})
    if 'ni' in ds.variables:
        ds = ds.rename({'ni': 'i', 'nj': 'j'})
    if 'nav_lat' in ds.variables:
        ds = ds.rename({'nav_lat': 'latitude', 'nav_lon': 'longitude'})
    if 'x' in ds.variables:
        ds = ds.rename({'x': 'i', 'y': 'j'})
    if 'x' in ds.dims:
        ds = ds.rename({'x': 'i', 'y': 'j'})
    ds = ds.chunk({'time': ds.dims['time'], 'i': 100, 'j': 100})
    ds['siconc'] = ds.siconc * 1e-2
    return ds


def find_areacello_file(model):
    files = glob.glob(os.path.join(AREACELLO_PATH, f"areacello_*_{model}_*.nc"))
    if not files:
        raise Exception(f"No areacello file for {model}")
    return files[0]


def get_areacello(filepath, verbose=False):
    '''Returns xarray.Dataset containing ocean gridcell area'''
    if verbose: print(f"Getting ocean cell area from {area_file}")
    ds = xr.open_dataset(filepath, use_cftime=True)
    if 'nlat' in ds.variables:
        ds = ds.rename({'nlat': 'j', 'nlon': 'i'})  # rename nlat and nlon dimensions to match siconc
    if 'nav_lat' in ds.variables:
        ds = ds.rename({'nav_lat': 'latitude', 'nav_lon': 'longitude'})
    if 'lat' in ds.variables:
        ds = ds.rename({'lat': 'latitude', 'lon': 'longitude'})
    if 'x' in ds.variables:
        ds = ds.rename({'x': 'i', 'y': 'j'})
    if 'x' in ds.dims:
        ds = ds.rename({'x': 'i', 'y': 'j'})
    if any([substr in filepath for substr in ['FGOALS-f3-L', 'FGOALS-g3']]):
        ds['j'] = list(reversed(ds.indexes['j']))
    ds = ds.chunk({'i': 100, 'j': 100})
    ds['areacello'] = ds.areacello * 1e-6  # convert from m^2 to km^2
    return ds


def cfmonth2datetime(old_time):
    """Converts CFtime object for month to datetime"""
    return [dt.datetime(t.year, t.month, 1) for t in old_time.values]


def calc_siarean(siconc, area):
    """Returns xarray.DataArray of northern hemisphere sea ice area"""
    siarea = siconc.siconc.where(siconc.siconc > 0.) * area.areacello
    siarean = siarea.where(area.latitude > 0.).sum(dim=['j', 'i'])
    siarean['time'] = cfmonth2datetime(siarean.time) 
    return siarean


def calc_siextentn(siconc, area):
    """Returns xarray.DataArray of northern hemisphere sea ice area"""
    siextent = siconc.siconc.where(siconc.siconc > .15) * area.areacello
    siextentn = siextent.where(area.latitude > 0.).sum(dim=['j', 'i'])
    siextentn['time'] = cfmonth2datetime(siextentn.time)
    return siextentn


def load_data(model, experiment, ensemble):
    '''Loads siconc and area data as xarray.Datasets'''
    try:
        siconc_files = find_siconc_files(model, experiment, ensemble)
    except Exception as error:
        raise Exception(error)
    
    try:
        areacello_file = find_areacello_file(model)
    except Exception as error:
        raise Exception(error)
        
    siconc_ds = get_siconc(siconc_files)
    area_ds = get_areacello(areacello_file)

    assert set(area_ds.areacello.dims).issubset(set(siconc_ds.siconc.dims)), f"{area_ds.areacello.dims} is not subset of {siconc_ds.siconc.dims} for {model}"
    assert 'latitude' in area_ds.variables and 'longitude' in area_ds.variables, f"latitude and longitude are not variables in areacello Dataset of {model}"
    assert 'latitude' in siconc_ds.variables and 'longitude' in siconc_ds.variables, f"latitude and longitude are not variables in siconc Dataset of {model}"
    assert 'i' in area_ds.areacello.dims and 'j' in area_ds.areacello.dims, f"Expect dimensions ('i', 'j') for areacello for {model}, found {area_ds.areacello.dims} instead"
    assert 'i' in siconc_ds.siconc.dims and 'j' in siconc_ds.siconc.dims, f"Expect dimensions ('i', 'j') for siconc for {model}, found {siconc_ds.areacello.dims} instead"

    return siconc_ds, area_ds
