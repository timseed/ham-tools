// Requires:
// Leaflet: http://leafletjs.com/
// Leaflet.curve: https://github.com/elfalem/Leaflet.curve
//
// Assumes:
// var map is a Leaflet map and already set up.

var latlngs = [];

var latlng1 = [data.coordinates[0][0], data.coordinates[0][1]],
	latlng2 = [data.coordinates[1][0], data.coordinates[1][1]];

var offsetX = latlng2[1] - latlng1[1],
	offsetY = latlng2[0] - latlng1[0];

var r = Math.sqrt( Math.pow(offsetX, 2) + Math.pow(offsetY, 2) ),
	theta = Math.atan2(offsetY, offsetX);

var thetaOffset = (3.14/10);

var r2 = (r/2)/(Math.cos(thetaOffset)),
	theta2 = theta + thetaOffset;

var midpointX = (r2 * Math.cos(theta2)) + latlng1[1],
	midpointY = (r2 * Math.sin(theta2)) + latlng1[0];

var midpointLatLng = [midpointY, midpointX];

latlngs.push(latlng1, midpointLatLng, latlng2);

var pathOptions = {
	color: 'rgba(255,255,255,0.5)',
	weight: 2
}

if (typeof document.getElementById('LEAFLET_MAP').animate === "function") {
	var durationBase = 2000;
   	var duration = Math.sqrt(Math.log(r)) * durationBase;
	// Scales the animation duration so that it's related to the line length
	// (but such that the longest and shortest lines' durations are not too different).
   	// You may want to use a different scaling factor.
  	pathOptions.animate = {
		duration: duration,
		iterations: Infinity,
		easing: 'ease-in-out',
		direction: 'alternate'
	}
}

var curvedPath = L.curve(
	[
		'M', latlng1,
		'Q', midpointLatLng,
			 latlng2
	], pathOptions).addTo(map);