import matplotlib.pyplot as plt

import cmip6.load as load
import cmip6.plotting as plotting

scale = 1e-6


def load_and_prepare_data(scenario, variable, experiment,
                          month=9, scale=1e-6):
    """Loads, subsets and scales ensemble data"""
    df = load.cmip6_ensemble_stats(scenario, experiment, variable)
    df = df[df.index.month == month]
    df = df * scale
    return df


def main(month=9, plotfile='cmip6_and_observed.png', verbose=True):
    """
    Generates plot of CMIP6 ensembles for 1900 to 2100 for SSPs with observations.
    Observations are from the Hadley-NSIDC combined sea ice index.

    :month: month number 1-12
    :plotfile: name of file to save plot

    """

    if verbose: print("Loading data")
    historical = load_and_prepare_data("historical", "siextentn", "r1i1p1f1",
                                       month=month, scale=1e-6)
    ssp370 = load_and_prepare_data("ssp370", "siextentn", "r1i1p1f1",
                                   month=month, scale=1e-6)
    ssp585 = load_and_prepare_data("ssp585", "siextentn", "r1i1p1f1",
                                   month=month, scale=1e-6)
    
    if verbose: print("Making plot")
    fig, ax = plotting.siextentn_filled(0., historical,
                                        [ssp370, ssp585],
                                        ['SSP370', 'SSP585'])

    plt.show()

    return


if __name__ == "__main__":
    main()
