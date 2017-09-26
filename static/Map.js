var map;
var points = [];

var seen_points = [];

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 28, lng: -83.27},
    zoom: 7
  });

  //stolen from StackOverflow just to get json file and see what parse does
  var client = new XMLHttpRequest();
  client.open('GET', '../static/temp1.json');
  client.responseType = "json";

  client.onreadystatechange = function() {
    if(client.readyState === XMLHttpRequest.DONE && client.status === 200) {
        objects = client.response;
		console.log(objects.length)
		console.log(objects[0])
        objects.forEach(function(item, index){
           addPoint(item);
        });

        console.log(objects.length);
        console.log(seen_points.length);
        console.log(seen_points);
    }
  }
  client.send();
}

/* Convert Tweet String into Map Marker */
function addPoint(tweet){
    //find location to place tweetText
    if(tweet.geo != null){
      // simple if a location is provided
      latitude = tweet.geo.coordinates[0];
      longitude = tweet.geo.coordinates[1];
    } else {
      //... if one is not get the bounding box for the place...
      bounding_box = tweet.place.bounding_box.coordinates;
      //... and set it in the center
      latitude = (bounding_box[0][0][1] + bounding_box[0][1][1])/2
      longitude = (bounding_box[0][0][0] + bounding_box[0][1][0])/2
    }

    var seen = false;
    //seeing how many tweets overlap
    seen_points.forEach(function(item){
        if(item[0] == latitude && item[1] == longitude){
          seen = true;
          item[3] = item[3] + 1;
        }
    });
    place_name = "";
    if(tweet.place != null)
      place_name = tweet.place.full_name;

    if(seen){
      console.log("Overlapping tweets");
    }else{
      seen_points.push([latitude, longitude, place_name, 1]);
    }

    //make sure we don't break due to a malformed tweet
    if(tweet.text == null)
        tweet.text = "";

    //create content string for displaying info about tweet
    contentString = '<div id="content">'+
             '<div id="siteNotice">'+
             '</div>'+
             '<h3 id="firstHeading" class="firstHeading">' + tweet.user.name + '</h3>'+
             'Followers: ' + tweet.user.followers_count +
             '<div id="bodyContent">'+
              tweet.text + '<br/>' +
             '</div>'+
             '</div>';

   marker = new google.maps.Marker({
    id: tweet.id,
    user_id: tweet.user.id,
    position: {lat: latitude, lng: longitude},
    map: map,
    infowindow: new google.maps.InfoWindow({
          content: contentString
    }),
    icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 4,
            strokeColor: "Orange"
          }
  });

  marker.addListener('click', function(e){
    this.infowindow.open(map, this);
  });

  points.push(marker);
}
