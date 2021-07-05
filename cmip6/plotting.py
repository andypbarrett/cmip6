import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

import datetime as dt

import numpy as np
import pandas as pd
COLOR = {
    'HISTORICAL': {'fill': '0.6', 'line': '0.2'},
    'SSP119': {'fill': '', 'line': 'purple'},
    'SSP126': {'fill': '', 'line': 'lime'},
    'SSP245': {'fill': 'lightblue', 'line': 'blue'},
    'SSP370': {'fill': '', 'line': 'yellow'},
    'SSP585': {'fill': 'pink', 'line': 'red'},
    }


def add_scenario(df, ax, label='', addline=True, fillcolor='0.6', linecolor='k',
                 linestyle='-'):
    """Plots polygon of mean+/-std scenario with mean line"""
    ax.fill_between(df.index, df.lower, df.upper, color=fillcolor)
    if addline:
        ax.plot(df.index, df['mean'],
                lw=3, linestyle=linestyle,
                color=linecolor,
                label=label)
    return ax

        
def siextentn_filled(observed, historical, ssp, ssp_names,
                     figsize=(12, 7)):
    """
    Generates plot of historical and future CMIP6 sea ice extent with observed extent
    from the combined Hadley-NSIDC series

    :observed: pandas.Dataframe containing observed sea ice extent
    :historical: pandas.Dataframe containing mean, upper and lower (mean+std and mean-std)
                 columns
    :ssp: a single pandas.Dataframe or list of pandas.Dataframes with SSP pathway dataframe
    :ssp_names: single string or list of strings containing labels for SSPs
    """
    # Prepend last date of historical to scenarios to make plot continuous
    fig, ax = plt.subplots(figsize=figsize)

    ax.set_xlim(dt.datetime(1900, 1, 1), dt.datetime(2100, 12, 31))
    ax.xaxis.set_ticks([dt.datetime(y, 1, 1) for y in np.arange(1920, 2100, 20)])

    ax.set_ylim(0, 10)
    ax.set_ylabel('10$^6$ km$^2$', fontsize=20)
    ax.tick_params(labelsize=20)

    add_scenario(historical, ax,
                      fillcolor=COLOR['HISTORICAL']['fill'],
                      linecolor=COLOR['HISTORICAL']['line'],
                      label='Historical')
    for scenario, name in zip(ssp, ssp_names):
        scenario = pd.concat([historical.last('1M'), scenario])  # makes lines continous
        add_scenario(scenario, ax,
                     fillcolor=COLOR[name]['fill'],
                     linecolor=COLOR[name]['line'],
                     label=name)
    
    ax.axhline(1, color='k')

    ax.text(0.02, 0.04, 'Stroeve and Barrett, National Snow and Ice Data Center', fontsize=12,
            transform=ax.transAxes)

    plt.legend(fontsize=18, bbox_to_anchor=(0, 0.6), loc='upper left', frameon=False)

    return fig, ax

