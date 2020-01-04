from pyesgf.search import SearchConnection
import json

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
    
