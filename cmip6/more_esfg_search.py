import requests
import json

URL = 'https://esgf-node.llnl.gov/esg-search/search/?offset=0&limit=200&type=Dataset&replica=false&latest=true&project=CMIP6&variable_id=siextentn&table_id=SImon&experiment_id=historical&member_id=r1i1p1f1&format=application%2Fsolr%2Bjson'

def main():

    page = requests.get(URL)
    data = page.json()

    for i, d in enumerate(data['response']['docs']):
        #print (f'{i} {d["source_id"]} {d["member_id"]}  {d["master_id"]}')
        for k, v in d.items():
            print (f'{k}: {v}')
        break

if __name__ == "__main__":
    main()

