const craigslist = require("node-craigslist");
const terms = process.argv[2];
console.log(terms);

let client = new craigslist.Client({
    baseHost : 'craigslist.com',
    city : "WashingtonDC"
});

var options = {
    baseHost : '',
    category : 'syp', //computer parts
    city : 'washingtondc',
    maxAsk : '',
    minAsk : '',
};

function filterListings(listings) {
    var out = [];

    for (var i = 0; i < listings.length; i++) {
        if(listings[i]["title"].toLowerCase().indexOf(terms.toLowerCase()) !== -1) {
            out.push(listings[i]);
        }
    }
    return out;
}

client
  .search(options, terms)
  .then((listings) => {
    // filtered listings (by price) 
    console.log(listings.length);
    console.log(filterListings(listings));
  })
  .catch((err) => {
    console.error(err);
  });

