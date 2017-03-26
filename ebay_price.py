from ebaysdk.finding import Connection
from pprint import pprint
import sync
import json
import sys
import numpy as np
import time
import subprocess
import threading

#sandbox
#api = Connection(domain='svcs.sandbox.ebay.com', appid="DylanJon-BigMarke-SBX-8007cb151-1613a88c", config_file=None)
#production
api = Connection(appid="DylanJon-BigMarke-PRD-8240e526c-b1c796ea", config_file=None)
cache = []

def get_price(keywords : str, category : str = 'Computer parts'):
    keywords = keywords.lower()
    cached = get_data_from_bigparser(keywords)
    if cached is not None:
        return cached
    request =  {
                'keywords': keywords,
                'itemFilter': [
                    {'name': 'SoldItemsOnly',
                     'value': 1},
                ],
                'sortOrder' : 'EndTimeSoonest',
                }
    resp = api.execute('findCompletedItems', request).dict()
    items = resp['searchResult']['item']

    arr = []

    for item in items:
        if '_currencyID' not in item['sellingStatus']['currentPrice'] or item['sellingStatus']['currentPrice']['_currencyID'] == 'USD':
            arr.append(float(item['sellingStatus']['currentPrice']['value']))
    data = {
            'price' : (sum(arr) / len(arr)) * 0.9, # ebay has 10% premium fee
            'stdev' : np.std(arr),
           }
    # bigparser writes are slow; do it in a thread
    t = threading.Thread(target=update_bigparser, args = (keywords, data))
    t.start()

    return data

def get_data_from_bigparser(keywords : str):
    r = subprocess.run(['sh', 'request.sh', 'get', keywords], check=True, stdout=subprocess.PIPE)
    resp = json.loads(r.stdout)
    if 'count' not in resp.keys():
        return None
    return {
            'price': resp['rows'][0]['data'][1],
            'stdev': resp['rows'][0]['data'][2]
           }

def update_bigparser(keywords, data):
    curtime = round(time.time())
    arr = [keywords, data['price'], data['stdev'], str(curtime)]
    i = open("out.csv", 'a')
    for x in arr:
        i.write((str(x) if type(x) != str else x) + ',')
    i.write('\n')
    i.close()
    sync.main()


if __name__ == '__main__':
    #print (f'Average market price for {sys.argv[1]} is {get_price(sys.argv[1])}')
    print('Average market price for {} is {}'.format((sys.argv[1]), (get_price(sys.argv[1]))))

#pprint(items)
