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


def main():

    conn = SearchConnection('https://esgf-data.dkrz.de/esg-search', distrib=True)
    ctx = conn.new_context(project='CMIP6',
                           experiment_id='historical',
                           variable=['siconc', 'sivol'],
                           frequency='mon')

    # For testing
    print(f'# Ensembles: {ctx.hit_count}')
    result = ctx.search()
    for r in result:
        print(r.dataset_id)
        
    return

    data = {}  # initialize dict
    data['ensembles'] = [r.json for r in ctx.search()]

    with open('model.txt', 'w') as outfile:
        json.dump(data, outfile)
    

    return

    
if __name__ == "__main__":
    main()
    
