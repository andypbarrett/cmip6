import requests
import json
import os

import datetime as dt

URL = 'https://esgf-node.llnl.gov/esg-search/search/?offset=0&limit=200&type=Dataset&replica=false&latest=true&project=CMIP6&variable_id=siextentn&table_id=SImon&experiment_id=historical&member_id=r1i1p1f1&format=application%2Fsolr%2Bjson'

node = 'https://esgf-node.llnl.gov/esg-search/'
api_keys = ['project', 'variable_id', 'table_id', 'experiment_id', 'member_id', 'limit']


def _build_search(variable, experiment, project='CMIP6', table='SImon', member=None, limit=500):
    '''Builds a search string for ESGF Search API'''
    search_parameters = []
    for k, v in zip(api_keys, [project, variable, table, experiment, member, limit]):
        if v:
            search_parameters.append(f'{k}={v}')
    return '&'.join(search_parameters)
    
def search(variable, experiment, project='CMIP6', table='SImon', member=None, limit=500):

    # Build search URL
    search_string = _build_search(variable, experiment, project, table, member, limit)
    URL = node + 'search/?' + search_string + '&format=application%2Fsolr%2Bjson'
    
    page = requests.get(URL)
    data = page.json()

    return data


def wget(variable, experiment, project='CMIP6', table='SImon', member=None, limit=500, dirpath="."):
    '''Gets a wget script'''
    search_string = _build_search(variable, experiment, project, table, member, limit)
    URL = node + 'wget?' + search_string
    page = requests.get(URL)
    #filen = os.path.join(".", f"wget_{dt.datetime.now().isoformat()}.sh")
    filen = os.path.join(".", f"wget_{project}_{variable}_{experiment}_{table}_{member}.sh")
    print(f"Writing download script to {filen}")
    with open(filen, "wb") as f:
        f.write(page.content)
    return


def print_search_short(data):
    '''Prints a summary of results'''
    for i, d in enumerate(data['response']['docs']):
        print (f'{i} {d["source_id"]} {d["member_id"]}  {d["master_id"]}')


def main(variable, experiment, project='CMIP6', table='SImon', member=None, limit=500,
         dosearch=True, dowget=False, dump_search=False):

    if dowget:
        wget(variable, experiment, project=project, table=table, member=member,
                      limit=limit)
    else:
        data = search(variable, experiment, project=project, table=table, member=member,
                      limit=limit)
        print_search_short(data)
        if dump_search:
            print("Does nothing right now")
    
    return

    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Searchs esgf-node.llnl.gov for CMIP6 model data')
    parser.add_argument('variable', type=str, help='variable name')
    parser.add_argument('experiment', type=str, help='experiment id')
    parser.add_argument('--project', type=str, default='CMIP6',
                        help='Name of project.  Default is CMIP6')
    parser.add_argument('--table', type=str, default='SImon',
                        help='parameter table, default=SImon')
    parser.add_argument('--member', type=str, default=None,
                        help='ensemble member: e.g. r1i1p1f1.  Default is to return all members')
    parser.add_argument('--limit', type=int, default=500,
                        help='Maximum number of results to return.  Default=500')
    parser.add_argument('--search', action='store_false', help='Do search')
    parser.add_argument('--wget', action='store_true', help='Get wget download script')
    args = parser.parse_args()

    main(args.variable, args.experiment, project=args.project, table=args.table,
           member=args.member, limit=args.limit, dosearch=args.search, dowget=args.wget)

