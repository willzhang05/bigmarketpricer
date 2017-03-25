const craigslist = require('node-craigslist');
 
var client = new craigslist.Client({
	baseHost : 'craigslist.org',
	city : 'washingtondc'
});


client.list().then((listings) => {
    // play with listings here... 
    listings.forEach((listing) => console.log(client.details(listing)));
  })
  .catch((err) => {
    console.error(err);
  });

