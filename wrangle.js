const searchTerm = process.argv[2];
const argv = require('minimist')(process.argv.slice(3));
console.log('Searching for: ' + searchTerm);

const options = {
    baseHost: ('baseHost' in argv ? argv['baseHost'] : 'craigslist.org'),  // default org
    category: ('category' in argv ? argv['category'] : ''),                // temporary syp
    city: ('city' in argv ? argv['city'] : 'washingtondc'),                // default dc
    maxAsk: ('maxAsk' in argv ? Math.ceil(argv['maxAsk']).toString() : ''),
    minAsk: ('minAsk' in argv ? Math.ceil(argv['maxAsk']).toString() : ''),
};

console.log('Options: ');
console.log(options);

const craigslist = require('node-craigslist');
const client = new craigslist.Client();

const numeral = require('numeral');

function compileListings(listings) {
    var promises = [];
    for (var i = 0; i < listings.length; i++)
        promises.push(client.details(listings[i]).catch((err) => { console.error(err); }));
    return Promise.all(promises).then((detailed) => {
        var compiled = [];
        for (var i = 0; i < listings.length; i++)
            compiled.push(Object.assign(listings[i], detailed[i])) return compiled;
    });
}

function filterListings(listings) {
    var filtered = [];
    for (var i = 0; i < listings.length; i++) {
        if (listings[i]['title'].toLowerCase().indexOf(searchTerm.toLowerCase()) === -1 ||
            listings[i]['price'] === '')
            continue;
        filtered.push(listings[i]);
    }

    return filtered.sort((a, b) => {
        var priceA = numeral(a.price).value();
        var priceB = numeral(b.price).value();
        if (priceA > priceB)
            return 1;
        else if (priceB > priceA)
            return -1;
        return 0;
    });
}

client.search(options, searchTerm)
    .then((listings) => {compileListings(filterListings(listings)).then((completed) => {
              console.log('%j', completed);
          })})
    .catch((err) => { console.error(err); });
