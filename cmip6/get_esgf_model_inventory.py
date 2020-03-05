from pyesgf.search import SearchConnection
import json

seaice_variables = [
    'siconc',  # (sea ice concentration %)
    'sithick',  # (floe ice thickness, for comparisons with observations)
    'sivol',  # (ice volume [m], *area of grid box gives sea ice volume per grid cell)
    'siage',  # (sea ice age)
    'sidconcdyn',  # (% change from dynamics)
    'sidconcth',  # (% change from thermodyncamics)
    'sidmassth',  # (mass change from thermodynamics)
    'sidmassdyn',  # (mass change from dynamics)
    'sispeed',  # (sea ice speed)
    'sidivvel',  # (sea ice divergence)
    'simassacrossline',  # (sea ice mass area flux through straits)
]

ocean_variables = [
    'mlotst',  # (ocean mixed layer thickness)
    'mlotstmax',  # (maximum mixed layer depth per month)
    'sos',  # (sea surface salinity)
    'tos',  # (sea surface temperature)
    'so',  # full depth salinity
    'to',  # full depth temperature
]


def get_inventory(context, verbose=False):
    '''
    Generates an inventory of CMIP6 data

    :context: dict of search terms
    
    :returns: dict repr of json data structure

    Example
    -------
    context = {'experiment_id': 'historical', 'variable': ['siconc', 'sivol'], 'frequency': 'mon'}
    table = get_inventory(context)
    '''
    conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
    ctx = conn.new_context(project='CMIP6',
                           experiment_id='historical',
                           variable=['siconc', 'sivol'],
                           frequency='mon')
    if verbose:
        print(f'# Hits: {ctx.hit_count}')

    data = {}  # initialize dict
    if ctx.hit_count > 0:
        data['ensembles'] = [r.json for r in ctx.search()]

    return data


def write_inventory(data, outfile):
    '''
    Writes inventory to JSON file

    :data: dict from json structure
    :outfile: filepath for outfile
    '''
    with open(outfile, 'w') as fo:
        json.dump(data, fo)

        
def main():

    context = {}

    result = get_inventory(context, verbose=True)
    write_inventory(result, 'seaice_list.txt')
    
    # For testing
#    for r in result:
#        print(r['dataset_id'])
        
    return

    
if __name__ == "__main__":
    main()
    
