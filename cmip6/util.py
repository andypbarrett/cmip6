"""Utilities for processing CMIP6"""


def lower(x):
    """Returns maximum of mean-std and 0."""
    return min(0., x.mean() - x.std())


def upper(x):
    """Returns mean + std"""
    return x.mean() + x.std()


def get_ensemble_stats(df):
    """Wrapper for pandas apply function

    :df: pandas.DataFrame containing ensemble of Arctic sea ice variables

    :returns: pandas.DataFrame containing ensemble mean and std, and upper and lower bounds
              of ensemble.
    """
    return df.apply(['mean', 'std', 'min', 'max', lower, upper], axis=1)
