from ebaysdk.finding import Connection
from pprint import pprint
import sys
import numpy as np

#sandbox
#api = Connection(domain='svcs.sandbox.ebay.com', appid="DylanJon-BigMarke-SBX-8007cb151-1613a88c", config_file=None)
#production
api = Connection(appid="DylanJon-BigMarke-PRD-8240e526c-b1c796ea", config_file=None)

def get_price(keywords : str, category : str = 'Computer parts'):
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

    return {
            'price' : (sum(arr) / len(arr)) * 0.9, # ebay has 10% premium fee
            'stdev' : np.std,
           }


if __name__ == '__main__':
    pass
    #print (f'Average market price for {sys.argv[1]} is {get_price(sys.argv[1])}')
    
#pprint(items)
