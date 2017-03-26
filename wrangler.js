const args = process.argv;
const searchTerm = args[2];


const options = {
    baseHost: 'craigslist.org', 
    category: (args.length >= 5 ? args[4] : ''),             
    city: 'washingtondc',             
    maxAsk: (args.length >= 4 ? Math.ceil(args[3]).toString() : ''),
    minAsk: '',
};

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
            compiled.push(Object.assign(listings[i], detailed[i]));
	    return compiled;
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
    .then((listings) => {compileListings(filterListings(listings))
        .then((completed) => {
              console.log('%j', completed);
        })
    })
    .catch((err) => { 
        console.error(err); 
    });
