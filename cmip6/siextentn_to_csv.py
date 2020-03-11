import warnings
import re
import datetime as dt
import pandas as pd

import munge

DATADIR = '/home/apbarret/Data/CMIP6'

VARIABLE = 'siextentn'
TABLE = 'SImon'
EXPERIMENT = 'ssp585'
MEMBER = 'r1i1p1f1'


def file_first_year(f):
    '''Returns first year of file from filename'''
    datestr = re.search('(\d{6})-\d{6}\.nc', f).groups()[0]
    date = dt.datetime.strptime(datestr, '%Y%m')
    return date.year


def make_dataframe(catalog):
    '''Builds a pandas DataFrame'''
    return


def siextentn_to_csv():
    '''Makes a pandas DataFrame of 1D data'''

    warnings.simplefilter("ignore")  # Brute force way to ignore RuntimeWarning
                                     # about converting from noleap calendar

    catalog = munge.generate_catalog(VARIABLE, TABLE, EXPERIMENT, MEMBER, datadir=DATADIR)
    
    series = []
    for model, modelfiles in catalog.items():
        modelfiles = [f for f in modelfiles if file_first_year(f) < 2100]
        if modelfiles:
            ds = munge.read_ensemble(modelfiles)
            ts = munge.dataset2timeseries(ds[VARIABLE])
            ts.name = model
            series.append(ts)

    warnings.simplefilter("default")  # Turn warnings back on

    df = pd.concat(series, axis=1)
    print(df.head())

#df.to_csv(os.path.join(DATADIR, 'siextentn', 'SImon', 'siextentn.SImon.CMIP6.historical.csv'))

if __name__ == "__main__":
    siextentn_to_csv()
