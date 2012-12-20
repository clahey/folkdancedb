db = require("./dbaccess");
http = require("http");
path = require("path");
fs = require("fs");
require("./stringUtil");

readData = function(req, callback) {
    input = "";
    req.on('data', function(data) {
	input += data;
    });
    req.on('end', function() {
	callback(input);
    });
}

parseEvening = function(data) {
    externalEvening = JSON.parse(data);
    evening = {};
    evening.dances = [];
    if (externalEvening.dances &&
	externalEvening.dances.forEach) {
	externalEvening.dances.forEach(function(danceId) {
	    if (typeof(danceId) == "string") {
		evening.dances.push(danceId);
	    } else {
		return null;
	    }
	});
    } else {
	return null;
    }
    return evening;
}

server = http.createServer(function(req, res) {
    db.whenReady(function(err) {
	switch (req.method) {
	case "GET":
	    if (req.url.startsWith("/data/list")) {
		query = req.url.substr("/data/list".length);
		if (query == "") {
		    db.dancecollection.find().toArray(function(err, dances) {
			if (err) {
			    res.writeHead(400);
			    res.write("Search Error.");
			    res.end();
			} else {
			    response = { "query" : "",
					 "result" : [] };
			    dances.forEach(function(dance) {
				response.result.push(
				    {
					"id": dance._id,
					"href" : "dance/" + dance._id,
					"title" : dance.title
				    });
			    });
			    res.writeHead(200);
			    res.write(JSON.stringify(response));
			    res.end();
			}
		    });
		} else {
		    res.writeHead(400);
		    res.write("Don't support specific queries yet.");
		    res.end();
		}
	    } else if (req.url.startsWith("/data/evening/")) {
		id = req.url.substr("/data/evening/".length);
		if (id == "") {
		    db.eveningcollection.find().toArray(function(err, evenings) {
			if (err) {
			    res.writeHead(400);
			    res.write("Search Error.");
			    res.end();
			} else {
			    response = { "query" : "",
					 "result" : [] };
			    evenings.forEach(function(evening) {
				response.result.push(
				    {
					"id": evening._id,
					"href" : "evening/" + evening._id,
				    });
			    });
			    res.writeHead(200);
			    res.write(JSON.stringify(response));
			    res.end();
			}
		    });
		} else {
		    db.eveningcollection.find({"_id" : db.mongo.ObjectID(id)})
			.toArray(function(err, evenings) {
			    if (err) {
				res.writeHead(400);
				res.write("Search Error.");
			    } else {
				if (evenings.length == 1) {
//				    forEach(evenings[0].dances,
//					    function(danceId) {
//						db.getDance(danceId,
//							    function(dance) {
//							    });
//					    });
//				    }
				    res.writeHead(200);
				    res.write(JSON.stringify(evenings[0]));
				} else {
				    res.writeHead(404);
				    res.write("No evenings found.");
				}
			    }
			    res.end();
			});
		}
	    } else if (req.url.startsWith("/data/dance/")) {
		id = req.url.substr("/data/dance/".length);
		db.dancecollection.find({"_id" : db.mongo.ObjectID(id)})
		    .toArray(function(err, dances) {
			if (err) {
			    res.writeHead(400);
			    res.write("Search Error.");
			} else {
			    if (dances.length == 1) {
				res.writeHead(200);
				res.write(JSON.stringify(dances[0]));
			    } else {
				res.writeHead(404);
				res.write("No evenings found.");
			    }
			}
			res.end();
		    });
	    } else {
		filename = path.normalize(path.join("clientCode", req.url));
		if (filename == "clientCode/") {
		    filename = "clientCode/index.html";
		}
		if (filename.startsWith("clientCode")) {
		    fs.readFile(filename, function(err, data) {
			if (err) {
			    res.writeHead(404);
			    res.write("File not found.");
			} else {
			    contentType = undefined;
			    if (path.extname(filename) == ".js") {
				res.writeHead(
				    200,
				    { 'Content-Type': 'text/javascript' });
			    } else if (path.extname(filename) == ".css") {
				res.writeHead(200,
					      { 'Content-Type': 'text/css' });
			    } else {
				res.writeHead(200);
			    }
			    res.write(data);
			}
			res.end();
		    });
		} else {
		    res.statusCode = 404;
		    res.write("File not found.");
		    res.end();
		}
	    }
	    break;
	case 'POST':
	    if (req.url == "/data/evening/") {
		readData(req, function(data) {
		    evening = parseEvening(data);
		    console.log(evening);
		    if (evening == null) {
			res.writeHead(400);
			res.write("Invalid evening.");
			res.end();
			return;
		    }
		    db.eveningcollection.insert(evening, function(err, docs) {
			if (err) {
			    res.writeHead(500);
			    res.write("Unable to insert.");
			} else {
			    res.writeHead(200);
			}
			res.end();
		    });
		});
	    }
	    break;
	case 'PUT':
	    if (req.url.startsWith("/data/evening/")) {
		id = req.url.substr("/data/evening/".length);
		readData(req, function(data) {
		    evening = parseEvening(data);
		    if (evening == null) {
			res.writeHead(400);
			res.write("Invalid evening.");
			res.end();
			return;
		    }
		    db.eveningcollection.update(
			{ _id: evening._id },
			evening,
			/*upsert*/ true,
			function(err) {
			    if (err) {
				res.writeHead(500);
				res.write("Unable to insert.");
			    } else {
				res.writeHead(200);
			    }
			    res.end();
			});
		});
	    }
	    break;
	}
    });
});

server.listen(8080, function() { console.log("ready"); });