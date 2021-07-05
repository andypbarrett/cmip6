"""Utilities for processing CMIP6"""


def lower(x):
    """Returns maximum of mean-std and 0."""
    return min(0., x.mean() - x.std())


def upper(x):
    """Returns mean + std"""
    return x.mean() + x.std()
