"use strict"
var left = document.querySelector("#slideshow > .left"),
    right = document.querySelector("#slideshow > .right"),
    ss = document.querySelector("#slideshow");


var script = document.createElement("script"),
    linkArr = [],
    index = Math.floor(Math.random() * 100);

script.src = "https://api.flickr.com/services/rest/?method=flickr.people.getPhotos&api_key=95bc9ba34511c5c6b3f35fb973f3cd92&user_id=144387717%40N03&extras=url_c%2Curl_o&format=json";
document.getElementById("wrapper").appendChild(script);

function jsonFlickrApi(data) {
    var photos = data.photos.photo;
    for (var i = 0; i < photos.length; i++) {
        linkArr.push([photos[i].url_c, photos[i].url_o]);
        //console.log(photos[i].url_c);
    }
    ss.lastElementChild.src = linkArr[index][0];
}

function getLeftImage() {
    if(index > 0) {
        index--;
    }
    console.log(index);
    console.log(ss.lastElementChild.src);
    ss.lastElementChild.src = linkArr[index][0];
}

function getRightImage() {
    if(index < linkArr.length - 1) {
        index++;
    }
    console.log(index);
    console.log(ss.lastElementChild.src);
    ss.lastElementChild.src = linkArr[index][0];
}


left.addEventListener("click", function(){getLeftImage()}, false);
right.addEventListener("click", function(){getRightImage()}, false);
left.addEventListener("touchleave", function(){getLeftImage()}, false);
right.addEventListener("touchleave", function(){getRightImage()}, false);
