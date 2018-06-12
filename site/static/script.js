var color = "maroon";

// A formatter for counts.
var formatCount = d3.format(",.0f");

var margin = {top: 20, right: 30, bottom: 30, left: 30},
    width = 700 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var features = [
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
]

// define the range for features
// absence = no bounds
var feature_bounds = {
  'acousticness': [0, 1.0],
  'danceability': [0, 1.0],
  'energy': [0, 1.0],
  'instrumentalness': [0, 1.0],
  'key': [0, 12],
  'liveness': [0, 1.0],
  'loudness': [-70, 0],
  'mode': [0, 1],
  'speechiness': [0, 1.0],
  'time_signature': [0, 12],
  'valence': [0, 1.0],
}

function loadGraph(trait) {
  d3.json("/static/top_tracks.json", function(data) { 
    var values = data.map(x => x[trait]);

    var bound
    if (trait in feature_bounds) {
      bound = feature_bounds[trait]
    } else { 
      let max = d3.max(values);
      let min = d3.min(values);
      bound = [min, max];
    }

    var x = d3.scale.linear()
          .domain(bound)
          .range([0, width]);

    var numBins = 10;

    var data = d3.layout.histogram()
        .bins(x.ticks(numBins))
        (values);

    var yMax = d3.max(data, function(d){return d.length});
    var y = d3.scale.linear()
        .domain([0, yMax])
        .range([height, 0]);

    d3.select("svg").remove()
    // define the canvas of the graph
    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var bar = svg.selectAll(".bar")
        .data(data)
      .enter().append("g")
        .attr("class", "bar")
        .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

    // Create the rectangles of the histogram
    bar.append("rect")
        .attr("x", 1)
        .attr("width", (x(data[0].dx) - x(0)) - 1)
        .attr("height", function(d) { return height - y(d.y); })
        .attr("fill", function(d) { return d3.rgb(color) });

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
  });
}
loadGraph("key")

window.onload = function() {
  let feature = document.getElementById("feature")
  for (let i = 0; i < features.length; i++) {
    let option = document.createElement("option");
    option.text = features[i];
    feature.add(option);
  }
  feature.onchange = function() {
    loadGraph(feature.value)
  }
}
