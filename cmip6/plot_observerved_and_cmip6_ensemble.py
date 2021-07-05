import matplotlib.pyplot as plt

import cmip6.load as load
import cmip6.plotting as plotting

scale = 1e-6

def main(month=9, plotfile='cmip6_and_observed.png', verbose=True):
    """
    Generates plot of CMIP6 ensembles for 1900 to 2100 for SSPs with observations.
    Observations are from the Hadley-NSIDC combined sea ice index.

    :month: month number 1-12
    :plotfile: name of file to save plot

    """

    if verbose: print("Loading data")
    historical = load.cmip6_ensemble_stats("historical", "r1i1p1f1")
    historical = historical[historical.index.month == month]
    historical = historical * scale

    ssp370 = load.cmip6_ensemble_stats("ssp370", "r1i1p1f1")
    ssp370 = ssp370[ssp370.index.month == month]
    ssp370 = ssp370 * scale
    
    if verbose: print("Making plot")
    fig, ax = plotting.siextentn_filled(0., historical, ssp370, 'SSP370')

    plt.show()

    return


if __name__ == "__main__":
    main()
