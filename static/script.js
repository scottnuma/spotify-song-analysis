var colors = ["maroon", "navy"];

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

var featureDescriptions = {
  'acousticness': "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
  'danceability': "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
  'duration_ms': "The duration of the track in milliseconds.",
  'energy': "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
  'instrumentalness': "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
  'key': "The key the track is in. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.",
  'liveness': "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
  'loudness': "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.",
  'mode': "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.",
  'speechiness': "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
  'tempo': "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
  'time_signature': "An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).",
  'valence': "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
};

// define the range for features
// absence = no bounds
var feature_bounds = {
  'acousticness': [0, 1.0],
  'danceability': [0, 1.0],
  'energy': [0, 1.0],
  'instrumentalness': [0, 1.0],
  'key': [0, 12],
  'liveness': [0, 1.0],
  'mode': [0, 1],
  'speechiness': [0, 1.0],
  'time_signature': [0, 12],
  'valence': [0, 1.0],
}

function loadGraphs(trait, time_frame_a, time_frame_b, username) {
  filepath = "/static/user_tracks/" + username + ".json"
  d3.json(filepath, function(raw_data) { 
    time_frames = [time_frame_a, time_frame_b];

    var values = [];
    for (i = 0; i < time_frames.length; i++) {
      values[i] = raw_data['top_tracks'][time_frames[i]].map(x => x[trait]);
    }

    var bound
    if (trait in feature_bounds) {
      bound = feature_bounds[trait]
    } else { 
      let max = Math.max(d3.max(values[0]), d3.max(values[1]));
      let min = Math.min(d3.min(values[0]), d3.min(values[1]));
      bound = [min, max];
    }

    var x = d3.scale.linear()
          .domain(bound)
          .range([0, width]);

    var numBins = 10;

    var data = []
    for (i = 0; i < values.length; i++) {
      data[i] = d3.layout.histogram()
          .bins(x.ticks(numBins))
          (values[i]);
    }

    var yMax = d3.max(data[0], function(d){return d.length});
    yMax = Math.max(yMax, d3.max(data[1], function(d){return d.length}));
    var y = d3.scale.linear()
        .domain([0, yMax])
        .range([height, 0]);

    d3.selectAll("svg > *").remove();
    // define the canvas of the graph
    var svg = d3.select("body").select("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var bar;
    for (i = 0; i < data.length; i++) {
      bar = svg.selectAll(".bar" + i)
          .data(data[i])
        .enter().append("g")
          .attr("class", "bar" + i)
          .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

      // Create the rectangles of the histogram
      bar.append("rect")
          .attr("x", 1)
          .attr("width", (x(data[i][0].dx) - x(0)) - 1)
          .attr("height", function(d) { return height - y(d.y); })
          .attr("fill", function(d) { return d3.rgb(colors[i]) })
          .attr("fill-opacity", .5);
    }

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

  // Load the description
  document.getElementById("description").innerHTML = featureDescriptions[feature.value]
}

window.onload = function() {
  // populate the selector with the different features
  let feature = document.getElementById("feature")
  for (let i = 0; i < features.length; i++) {
    let option = document.createElement("option");
    option.text = features[i];
    feature.add(option);
  }

  let time_frame_a = document.getElementById("time_frame_a")
  let time_frame_b = document.getElementById("time_frame_b")

  var parsedUrl = new URL(window.location.href);
  username0 = parsedUrl.searchParams.get("username0");
  console.log(username0); 

  reload_graph = function() {
    loadGraphs(feature.value, time_frame_a.value, time_frame_b.value, username0);
  }
  feature.onchange = reload_graph
  time_frame_a.onchange = reload_graph
  time_frame_b.onchange = reload_graph
  loadGraphs("key", "short_term", "long_term", username0);
}
