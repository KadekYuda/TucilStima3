var data = [];
var edge = [];
var labelIdx = 0;
var prevIdx;

function initMap() {
  // Map Options

  var options =  {
    zoom: 16,
    center: {lat: -6.892, lng: 107.611}
  }

  //New Map
  var map = new google.maps.Map(document.getElementById('map'), options);

  //Listener for a click in a map, there will be a marker
  google.maps.event.addListener(map, 'click', function(event) {
     placeMarker(event.latLng);
  });

  //Place new marker
  function placeMarker(location) {
      var marker = new google.maps.Marker({
          position: location,
          map: map,
          id: labelIdx,
          label: (labelIdx++).toString()
      });
      data.push(location);

      google.maps.event.addListener(marker, "click", function(){
        var marker = this;
        //alert('ID is: ' + this.id)
        if (prevIdx == null){
          prevIdx = this.id
        } else {
          addPolyLine(prevIdx, this.id);
          prevIdx = this.id;
        }
      });
  }

  function contains(a, obj) {
    for (var i = 0; i < a.length; i++) {
        if (a[i].equals(obj)) {
            return true;
        }
    }
    return false;
  }

  function addPolyLine(start, end){
    if (start != end && !contains(edge,[start, end]) && !contains(edge,[end, start])){
      poly = new google.maps.Polyline({
        strokeColor: '#000000',
        strokeOpacity: 1.0,
        strokeWeight: 3
      });
      poly.setMap(map);
      var path = poly.getPath();
      path.push(data[start]);
      path.push(data[end]);
      edge.push([start, end]);
    }
  }
}

function sendData(){
  var obj = {'coordinates':data, 'edges':edge};
  document.getElementById("demo").innerHTML = data;
  $.ajax({
    url: '/postmethod',
    type: 'POST',
    data: JSON.stringify(obj),
    contentType: 'application/json',
    dataType: 'json',
    async: true,
    success: function(msg) {
        alert(msg);
    }
  });
}

// Warn if overriding existing method
if(Array.prototype.equals)
    console.warn("Overriding existing Array.prototype.equals. Possible causes: New API defines the method, there's a framework conflict or you've got double inclusions in your code.");
// attach the .equals method to Array's prototype to call it on any array
Array.prototype.equals = function (array) {
    // if the other array is a falsy value, return
    if (!array)
        return false;

    // compare lengths - can save a lot of time
    if (this.length != array.length)
        return false;

    for (var i = 0, l=this.length; i < l; i++) {
        // Check if we have nested arrays
        if (this[i] instanceof Array && array[i] instanceof Array) {
            // recurse into the nested arrays
            if (!this[i].equals(array[i]))
                return false;
        }
        else if (this[i] != array[i]) {
            // Warning - two different object instances will never be equal: {x:20} != {x:20}
            return false;
        }
    }
    return true;
}
// Hide method from for-in loops
Object.defineProperty(Array.prototype, "equals", {enumerable: false});
