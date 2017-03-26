const craigslist = require("node-craigslist");

const searchTerm = process.argv[2];
const argv = require('minimist')(process.argv.slice(3))
console.log(searchTerm);
console.log(argv);

var client = new craigslist.Client();

var options = {
    baseHost : ('baseHost' in argv ? argv['baseHost'] : ''),
    category : ('category' in argv ? argv['category'] : 'syp'), //temporary syp
    city : ('city' in argv ? argv['city'] : 'washingtondc'), //default dc
    maxAsk : ('maxAsk' in argv ? argv['maxAsk'] : ''),
    minAsk : ('minAsk' in argv ? argv['minAsk'] : ''),
};

console.log(options);

function filterListings(listings) {
    var out = [];

    for (var i = 0; i < listings.length; i++) {
        if(listings[i]["title"].toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1) {
            out.push(listings[i]);
        }
    }
    return out;
}

client.search(options, searchTerm)
  .then((listings) => {
    // filtered listings (by price) 
    console.log(listings.length);
    console.log(filterListings(listings));
  }).catch((err) => {
    console.error(err);
  });

