from ebaysdk.finding import Connection
from pprint import pprint
import sys

#sandbox
api = Connection(domain='svcs.sandbox.ebay.com', appid="DylanJon-BigMarke-SBX-8007cb151-1613a88c", config_file=None)
#production
api = Connection(appid="DylanJon-BigMarke-PRD-8240e526c-b1c796ea", config_file=None)

def get_price(keywords : str, category : str = 'Computer parts'):
    request =  {
                'keywords': keywords,
                'itemFilter': [
                    {'name': 'SoldItemsOnly',
                     'value': 1},
                ],
                }
    resp = api.execute('findCompletedItems', request).dict()
    items = resp['searchResult']['item']

    s = 0
    numItems = 0

    for item in items:
        if '_currencyID' not in item['sellingStatus']['currentPrice'] or item['sellingStatus']['currentPrice']['_currencyID'] == 'USD':
            s += float(item['sellingStatus']['currentPrice']['value'])
            numItems += 1
    return s / numItems


if __name__ == '__main__':
    print (f'Average market price for {sys.argv[1]} is {get_price(sys.argv[1])}')
#pprint(items)
