# Module containing functions to process CMIP6 data
import os
import glob
import warnings
import datetime as dt

import xarray as xr


def read_ensemble(filelist):
    '''Reads file for a given model ensemble into an xarray Dataset'''
    ds = xr.open_mfdataset(filelist, combine='by_coords')
    if isinstance(ds.indexes['time'], xr.CFTimeIndex):
        ds['time'] = ds.indexes['time'].to_datetimeindex()
    return ds


def _normalize_datetime(TimeIndex):
    '''Sets timestamp for monthly data to YYYY-MM-15'''
    return [dt.datetime(y, m, 15) for y, m in zip(TimeIndex.year, TimeIndex.month)]


def dataset2timeseries(da):
    '''Converts ds.siextent to a pandas timeseries.  Times are set to midnight 00:00:00'''
    ts = da.squeeze().to_series()
    ts.index = _normalize_datetime(ts.index)
    return ts


def generate_catalog(variable, table, experiment, member, datadir='.'):
    '''
    Makes a dictionary of files for a given variable, table, experiment and member by model (source_id)
    '''
    models = [os.path.basename(d) for d in glob.glob(os.path.join(datadir, f"{variable}/{table}/*")) if os.path.isdir(d)]
    catalog = {}
    for m in models:
        catalog[m] = glob.glob(os.path.join(datadir, variable, table, m, experiment, member, '*.nc'))
    return catalog




