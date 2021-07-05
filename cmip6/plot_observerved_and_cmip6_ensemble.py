import cmip6.load as load
import cmip6.plotting as plotting


def main(month=9, plotfile='cmip6_and_observed.png', verbose=True):
    """
    Generates plot of CMIP6 ensembles for 1900 to 2100 for SSPs with observations.
    Observations are from the Hadley-NSIDC combined sea ice index.

    :month: month number 1-12
    :plotfile: name of file to save plot

    """

    if verbose: print("Loading data")
    historical = load.cmip6_ensemble("historical", "r1i1p1f1")
    print(historical)
    
    fig, ax = plotting.siextentn_filled(0., historical, 0., '')

    fig.show()

    return


if __name__ == "__main__":
    main()
